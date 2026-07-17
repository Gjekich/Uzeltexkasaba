// Uzeltexkasaba Public Portal - Main Javascript Logic

const API_BASE = '/api';

// DOM Ready
document.addEventListener('DOMContentLoaded', () => {
    highlightActiveLink();
    initContactForm();
    loadLatestNews();
});

// Highlight Active Nav Link
function highlightActiveLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (currentPath.includes(href) && href !== 'index.html' && href !== '/') {
            link.classList.add('active');
        } else if ((currentPath === '/' || currentPath.endsWith('index.html')) && (href === 'index.html' || href === '/')) {
            link.classList.add('active');
        }
    });
}

// Toast Notifications Helper
function showToast(message, type = 'info') {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let icon = 'ℹ️';
    if (type === 'success') icon = '✅';
    if (type === 'error') icon = '❌';
    
    toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 4000);
}

// Contact Form Submission
function initContactForm() {
    const form = document.getElementById('contactForm');
    if (!form) return;
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const fullName = document.getElementById('fullName').value.trim();
        const phone = document.getElementById('phone').value.trim();
        const message = document.getElementById('message').value.trim();
        
        if (!fullName || !phone || !message) {
            showToast("Iltimos, barcha maydonlarni to'ldiring.", "error");
            return;
        }
        
        const submitBtn = form.querySelector('button[type="submit"]');
        const origText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Yuborilmoqda...';
        
        try {
            const response = await fetch(`${API_BASE}/applications/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    full_name: fullName,
                    phone: phone,
                    message: message
                })
            });
            
            if (response.ok) {
                showToast("Murojaatingiz muvaffaqiyatli yuborildi. Tez orada siz bilan bog'lanamiz!", "success");
                form.reset();
            } else {
                const data = await response.json();
                showToast(data.detail || "Xatolik yuz berdi. Iltimos, qaytadan urunib ko'ring.", "error");
            }
        } catch (error) {
            console.error('Submission error:', error);
            showToast("Server bilan bog'lanishda xatolik yuz berdi.", "error");
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = origText;
        }
    });
}

// Fetch and load latest 3 news on Home Page
async function loadLatestNews() {
    const grid = document.getElementById('homeNewsGrid');
    if (!grid) return;
    
    try {
        const response = await fetch(`${API_BASE}/news/?page=1&size=3`);
        if (response.ok) {
            const newsList = await response.json();
            if (newsList.length === 0) {
                grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: var(--text-muted);">Hozircha yangiliklar yo\'q.</div>';
                return;
            }
            grid.innerHTML = newsList.map(news => {
                const firstImg = news.image_url ? news.image_url.split(',')[0] : '';
                const bgImage = firstImg ? `style="background-image: url('${firstImg}')"` : 'style="background-color: #1f2937;"';
                const date = new Date(news.created_at).toLocaleDateString('uz-UZ', { day: 'numeric', month: 'long', year: 'numeric' });
                
                return `
                    <div class="news-card">
                        <div class="news-img" ${bgImage}>
                            <span class="news-badge">Faoliyat</span>
                        </div>
                        <div class="news-body">
                            <span class="news-date">${date}</span>
                            <h3 class="news-title">${escapeHTML(news.title)}</h3>
                            <p class="news-excerpt">${escapeHTML(news.content)}</p>
                            <a href="news_detail.html?id=${news.id}" class="privilege-link" style="margin-top: 16px;">Batafsil ➔</a>
                        </div>
                    </div>
                `;
            }).join('');
        }
    } catch (error) {
        console.error('Failed to load news:', error);
    }
}

// HTML Escaping Helper
function escapeHTML(str) {
    if (!str) return '';
    return str.replace(/[&<>'"]/g, 
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag] || tag)
    );
}
