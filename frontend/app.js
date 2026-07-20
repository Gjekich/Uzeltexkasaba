// Uzeltexkasaba Public Portal - Main Javascript Logic

const API_BASE = '/api';

// DOM Ready
document.addEventListener('DOMContentLoaded', () => {
    highlightActiveLink();
    initContactForm();
    loadLatestNews();
    initLanguageSwitcher();
});

// Language Switcher Logic
function getCurrentLanguage() {
    return localStorage.getItem('preferred_language') || 'uz';
}

function setLanguage(lang) {
    if (typeof translations === 'undefined' || !translations[lang]) return;
    localStorage.setItem('preferred_language', lang);
    
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const attr = el.getAttribute('data-i18n-attr');
        if (translations[lang] && translations[lang][key]) {
            if (attr) {
                el.setAttribute(attr, translations[lang][key]);
            } else {
                el.innerText = translations[lang][key];
            }
        }
    });
    
    // Sync select elements
    document.querySelectorAll('.lang-select').forEach(sel => {
        sel.value = lang;
    });

    // Dynamic lists re-render on language switch
    if (typeof renderPrivileges === 'function' && typeof allPrivileges !== 'undefined') {
        renderPrivileges(allPrivileges);
    }
    if (typeof renderLegislations === 'function' && typeof allLegislations !== 'undefined') {
        renderLegislations(allLegislations);
    }
    if (typeof renderNews === 'function' && typeof allNews !== 'undefined') {
        renderNews(allNews);
    }
    if (typeof renderEvents === 'function' && typeof allEvents !== 'undefined') {
        renderEvents(allEvents);
    }
    if (typeof renderStaff === 'function' && typeof allStaff !== 'undefined') {
        renderStaff(allStaff);
    }
    if (typeof renderGallery === 'function') {
        renderGallery();
    }
    if (typeof renderGuide === 'function') {
        renderGuide();
    }
    if (typeof loadLatestNews === 'function') {
        loadLatestNews();
    }
}

function initLanguageSwitcher() {
    const currentLang = getCurrentLanguage();
    setLanguage(currentLang);
    
    document.querySelectorAll('.lang-select').forEach(sel => {
        sel.addEventListener('change', (e) => {
            setLanguage(e.target.value);
        });
    });
}

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
                const bgImage = firstImg ? `style="background-image: url('${firstImg}')"` : 'style="background-image: url(\'images/default_news.jpg\')"';
                const date = new Date(news.created_at).toLocaleDateString('uz-UZ', { day: 'numeric', month: 'long', year: 'numeric' });
                
                const title = getLocalizedField(news, 'title');
                const content = getLocalizedField(news, 'content');

                return `
                    <div class="news-card">
                        <div class="news-img" ${bgImage}>
                            <span class="news-badge" data-i18n="news_tag">Faoliyat</span>
                        </div>
                        <div class="news-body">
                            <span class="news-date">${date}</span>
                            <h3 class="news-title">${escapeHTML(title)}</h3>
                            <p class="news-excerpt">${escapeHTML(content)}</p>
                            <a href="news_detail.html?id=${news.id}" class="privilege-link" style="margin-top: 16px;" data-i18n="read_more">Batafsil ➔</a>
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

// Localized field helper for objects
function getLocalizedField(obj, field) {
    const lang = getCurrentLanguage();
    if (lang === 'uz') {
        return obj[field] || '';
    }
    const localized = obj[`${field}_${lang}`];
    return localized || obj[field] || '';
}

// Staff Position Translation Helper
function translatePosition(positionName) {
    if (!positionName) return '';
    const currentLang = getCurrentLanguage();
    if (currentLang === 'uz') return positionName;
    
    // Normalize position name (replace double spaces, trim)
    const normalized = positionName.replace(/\s+/g, ' ').trim().toLowerCase();
    
    const mapping = {
        ru: {
            "boshqaruvi raisi": "Председатель правления",
            "boshqaruvi raisining birinchi o'rinbosari": "Первый заместитель председателя правления",
            "boshqaruvi raisining o'rinbosari": "Заместитель председателя правления",
            "boshqaruvi raisining maslahatchisi": "Советник председателя правления",
            "boshqaruvi raisining yordamchisi": "Помощник председателя правления",
            "boshqarma boshlig'i": "Начальник управления",
            "bo'lim boshlig'i": "Начальник отдела",
            "bosh buxgalter": "Главный бухгалтер",
            "bosh mutaxassis": "Главный специалист",
            "yetakchi mutaxassis": "Ведущий специалист",
            "mutaxassis": "Специалист",
            "muhandisi": "Инженер",
            "haydovchi": "Водитель",
            "qozonxona operatori": "Оператор котельной",
            "bino farroshi": "Уборщик здания",
            "energetik-muhandis": "Инженер-энергетик",
            "qorovul": "Охранник",
            "ish yurituvchi": "Делопроизводитель",
            "arxivrius": "Архивариус"
        },
        en: {
            "boshqaruvi raisi": "Chairman of the Board",
            "boshqaruvi raisining birinchi o'rinbosari": "First Deputy Chairman of the Board",
            "boshqaruvi raisining o'rinbosari": "Deputy Chairman of the Board",
            "boshqaruvi raisining maslahatchisi": "Advisor to the Chairman of the Board",
            "boshqaruvi raisining yordamchisi": "Assistant to the Chairman of the Board",
            "boshqarma boshlig'i": "Head of Department",
            "bo'lim boshlig'i": "Head of Section",
            "bosh buxgalter": "Chief Accountant",
            "bosh mutaxassis": "Chief Specialist",
            "yetakchi mutaxassis": "Leading Specialist",
            "mutaxassis": "Specialist",
            "muhandisi": "Engineer",
            "haydovchi": "Driver",
            "qozonxona operatori": "Boiler Room Operator",
            "bino farroshi": "Building Cleaner",
            "energetik-muhandis": "Energy Engineer",
            "qorovul": "Guard",
            "ish yurituvchi": "Office Manager",
            "arxivrius": "Archivist"
        }
    };
    
    return (mapping[currentLang] && mapping[currentLang][normalized]) || positionName;
}
