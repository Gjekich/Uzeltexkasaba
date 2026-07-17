// Uzeltexkasaba Admin Dashboard - Javascript Control

let authToken = localStorage.getItem('admin_token') || '';
let currentTab = 'news';

// DOM Ready
document.addEventListener('DOMContentLoaded', () => {
    initAdmin();
});

function initAdmin() {
    if (authToken) {
        showDashboard();
    } else {
        showLoginCard();
    }

    // Set up Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    // Set up Tab switching
    const menuItems = document.querySelectorAll('.admin-menu-item');
    menuItems.forEach(item => {
        item.addEventListener('click', (e) => {
            menuItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            const tabName = item.getAttribute('data-tab');
            switchTab(tabName);
        });
    });

    // Forms submission handlers
    document.getElementById('newsForm').addEventListener('submit', submitNewsForm);
    document.getElementById('privilegeForm').addEventListener('submit', submitPrivilegeForm);
    document.getElementById('legislationForm').addEventListener('submit', submitLegislationForm);
    document.getElementById('staffForm').addEventListener('submit', submitStaffForm);
}

function showLoginCard() {
    document.getElementById('loginCard').style.display = 'block';
    document.getElementById('adminDashboard').style.display = 'none';
}

function showDashboard() {
    document.getElementById('loginCard').style.display = 'none';
    document.getElementById('adminDashboard').style.display = 'block';
    
    // Set admin name display
    const username = localStorage.getItem('admin_username') || 'Administrator';
    document.getElementById('adminUsernameDisplay').textContent = username;

    // Load initial tab data
    loadTabData(currentTab);
}

// Login Handler
async function handleLogin(e) {
    e.preventDefault();
    const usernameVal = document.getElementById('username').value.trim();
    const passwordVal = document.getElementById('password').value;

    const loginBtn = e.target.querySelector('button[type="submit"]');
    loginBtn.disabled = true;
    loginBtn.innerHTML = 'Yuklanmoqda...';

    // Format as URL encoded form data
    const formData = new URLSearchParams();
    formData.append('username', usernameVal);
    formData.append('password', passwordVal);

    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            authToken = data.access_token;
            localStorage.setItem('admin_token', authToken);
            localStorage.setItem('admin_username', usernameVal);
            
            showToast("Tizimga muvaffaqiyatli kirdingiz!", "success");
            showDashboard();
        } else {
            const err = await response.json();
            showToast(err.detail || "Login yoki parol xato!", "error");
        }
    } catch (error) {
        console.error(error);
        showToast("Serverga bog'lanib bo'lmadi.", "error");
    } finally {
        loginBtn.disabled = false;
        loginBtn.innerHTML = "Tizimga kirish";
    }
}

// Logout
function handleLogout() {
    authToken = '';
    localStorage.removeItem('admin_token');
    localStorage.removeItem('admin_username');
    showToast("Tizimdan chiqdingiz.", "info");
    showLoginCard();
}

// Switch tabs
function switchTab(tabName) {
    currentTab = tabName;
    const sections = document.querySelectorAll('.tab-section');
    sections.forEach(sec => sec.style.display = 'none');

    document.getElementById(`tab-${tabName}`).style.display = 'block';
    loadTabData(tabName);
}

// Load current tab data
function loadTabData(tab) {
    if (tab === 'news') loadNewsList();
    if (tab === 'privileges') loadPrivilegesList();
    if (tab === 'legislation') loadLegislationList();
    if (tab === 'applications') loadApplicationsList();
    if (tab === 'staff') loadStaffList();
}

/* ==========================================================================
   News CRUD
   ========================================================================== */
async function loadNewsList() {
    const tbody = document.getElementById('newsTableBody');
    tbody.innerHTML = '<tr><td colspan="4" style="text-align: center;">Yuklanmoqda...</td></tr>';

    try {
        const response = await fetch('/api/news/');
        if (response.ok) {
            const newsList = await response.json();
            if (newsList.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--text-muted);">Yangiliklar mavjud emas.</td></tr>';
                return;
            }

            tbody.innerHTML = newsList.map(news => {
                const imgHtml = news.image_url ? `<img src="${news.image_url}" style="width: 50px; height: 35px; object-fit: cover; border-radius: var(--radius-sm);">` : '—';
                const date = new Date(news.created_at).toLocaleDateString('uz-UZ');
                return `
                    <tr>
                        <td>${imgHtml}</td>
                        <td><strong>${escapeHTML(news.title)}</strong></td>
                        <td>${date}</td>
                        <td style="text-align: right;">
                            <button onclick="editNews(${news.id})" class="admin-action-btn btn-edit" title="Tahrirlash">✏️</button>
                            <button onclick="deleteNews(${news.id})" class="admin-action-btn btn-delete" title="O'chirish">🗑️</button>
                        </td>
                    </tr>
                `;
            }).join('');
        }
    } catch (e) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--color-danger);">Yuklashda xatolik.</td></tr>';
    }
}

function openNewsFormModal() {
    document.getElementById('newsForm').reset();
    document.getElementById('editNewsId').value = '';
    document.getElementById('newsFormTitle').textContent = "Yangi maqola qo'shish";
    document.getElementById('newsFormModal').classList.add('open');
}

function closeNewsFormModal() {
    document.getElementById('newsFormModal').classList.remove('open');
}

async function submitNewsForm(e) {
    e.preventDefault();
    const id = document.getElementById('editNewsId').value;
    const title = document.getElementById('newsTitleInput').value.trim();
    const content = document.getElementById('newsContentInput').value.trim();
    const imageUrl = document.getElementById('newsImageUrlInput').value.trim();

    const payload = { title, content, image_url: imageUrl || null };
    const method = id ? 'PUT' : 'POST';
    const url = id ? `/api/news/${id}` : '/api/news/';

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            showToast("Yangilik muvaffaqiyatli saqlandi!", "success");
            closeNewsFormModal();
            loadNewsList();
        } else {
            showToast("Saqlashda xatolik yuz berdi.", "error");
        }
    } catch (error) {
        showToast("Server xatoligi.", "error");
    }
}

async function editNews(id) {
    try {
        const response = await fetch(`/api/news/${id}`);
        if (response.ok) {
            const news = await response.json();
            document.getElementById('editNewsId').value = news.id;
            document.getElementById('newsTitleInput').value = news.title;
            document.getElementById('newsContentInput').value = news.content;
            document.getElementById('newsImageUrlInput').value = news.image_url || '';
            
            document.getElementById('newsFormTitle').textContent = "Maqolani tahrirlash";
            document.getElementById('newsFormModal').classList.add('open');
        }
    } catch (e) {
        showToast("Ma'lumotlarni yuklab bo'lmadi.", "error");
    }
}

async function deleteNews(id) {
    if (!confirm("Ushbu yangilikni o'chirib tashlamoqchimisiz?")) return;

    try {
        const response = await fetch(`/api/news/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        if (response.ok) {
            showToast("Muvaffaqiyatli o'chirildi.", "success");
            loadNewsList();
        } else {
            showToast("O'chirishda xatolik.", "error");
        }
    } catch (e) {
        showToast("Server xatoligi.", "error");
    }
}

/* ==========================================================================
   Privileges CRUD
   ========================================================================== */
async function loadPrivilegesList() {
    const tbody = document.getElementById('privilegesTableBody');
    tbody.innerHTML = '<tr><td colspan="4" style="text-align: center;">Yuklanmoqda...</td></tr>';

    try {
        const response = await fetch('/api/privileges/');
        if (response.ok) {
            const list = await response.json();
            if (list.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--text-muted);">Imtiyozlar mavjud emas.</td></tr>';
                return;
            }

            tbody.innerHTML = list.map(priv => `
                <tr>
                    <td style="font-size: 1.5rem;">${escapeHTML(priv.icon || '🎁')}</td>
                    <td><strong>${escapeHTML(priv.title)}</strong></td>
                    <td style="color: var(--text-secondary); max-width: 300px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${escapeHTML(priv.description)}</td>
                    <td style="text-align: right;">
                        <button onclick="editPrivilege(${priv.id})" class="admin-action-btn btn-edit">✏️</button>
                        <button onclick="deletePrivilege(${priv.id})" class="admin-action-btn btn-delete">🗑️</button>
                    </td>
                </tr>
            `).join('');
        }
    } catch (e) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--color-danger);">Yuklashda xatolik.</td></tr>';
    }
}

function openPrivilegeFormModal() {
    document.getElementById('privilegeForm').reset();
    document.getElementById('editPrivilegeId').value = '';
    document.getElementById('privilegeFormTitle').textContent = "Yangi imtiyoz qo'shish";
    document.getElementById('privilegeFormModal').classList.add('open');
}

function closePrivilegeFormModal() {
    document.getElementById('privilegeFormModal').classList.remove('open');
}

async function submitPrivilegeForm(e) {
    e.preventDefault();
    const id = document.getElementById('editPrivilegeId').value;
    const title = document.getElementById('privilegeTitleInput').value.trim();
    const description = document.getElementById('privilegeDescInput').value.trim();
    const icon = document.getElementById('privilegeIconInput').value.trim();
    const content = document.getElementById('privilegeContentInput').value.trim();

    const payload = { title, description, icon, content };
    const method = id ? 'PUT' : 'POST';
    const url = id ? `/api/privileges/${id}` : '/api/privileges/';

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            showToast("Imtiyoz muvaffaqiyatli saqlandi!", "success");
            closePrivilegeFormModal();
            loadPrivilegesList();
        } else {
            showToast("Saqlashda xatolik yuz berdi.", "error");
        }
    } catch (error) {
        showToast("Server xatoligi.", "error");
    }
}

async function editPrivilege(id) {
    try {
        const response = await fetch(`/api/privileges/${id}`);
        if (response.ok) {
            const priv = await response.json();
            document.getElementById('editPrivilegeId').value = priv.id;
            document.getElementById('privilegeTitleInput').value = priv.title;
            document.getElementById('privilegeDescInput').value = priv.description;
            document.getElementById('privilegeIconInput').value = priv.icon || '🎁';
            document.getElementById('privilegeContentInput').value = priv.content || '';
            
            document.getElementById('privilegeFormTitle').textContent = "Imtiyozni tahrirlash";
            document.getElementById('privilegeFormModal').classList.add('open');
        }
    } catch (e) {
        showToast("Ma'lumotlarni yuklab bo'lmadi.", "error");
    }
}

async function deletePrivilege(id) {
    if (!confirm("Ushbu imtiyozni o'chirib tashlamoqchimisiz?")) return;

    try {
        const response = await fetch(`/api/privileges/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        if (response.ok) {
            showToast("Muvaffaqiyatli o'chirildi.", "success");
            loadPrivilegesList();
        } else {
            showToast("O'chirishda xatolik.", "error");
        }
    } catch (e) {
        showToast("Server xatoligi.", "error");
    }
}

/* ==========================================================================
   Legislation CRUD
   ========================================================================== */
async function loadLegislationList() {
    const tbody = document.getElementById('legislationTableBody');
    tbody.innerHTML = '<tr><td colspan="4" style="text-align: center;">Yuklanmoqda...</td></tr>';

    try {
        const response = await fetch('/api/legislations/');
        if (response.ok) {
            const list = await response.json();
            if (list.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--text-muted);">Hujjatlar mavjud emas.</td></tr>';
                return;
            }

            tbody.innerHTML = list.map(leg => {
                const date = new Date(leg.created_at).toLocaleDateString('uz-UZ');
                return `
                    <tr>
                        <td><span class="leg-cat-badge">${escapeHTML(leg.category)}</span></td>
                        <td><strong>${escapeHTML(leg.title)}</strong></td>
                        <td>${date}</td>
                        <td style="text-align: right;">
                            <button onclick="editLegislation(${leg.id})" class="admin-action-btn btn-edit">✏️</button>
                            <button onclick="deleteLegislation(${leg.id})" class="admin-action-btn btn-delete">🗑️</button>
                        </td>
                    </tr>
                `;
            }).join('');
        }
    } catch (e) {
        tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: var(--color-danger);">Yuklashda xatolik.</td></tr>';
    }
}

function openLegislationFormModal() {
    document.getElementById('legislationForm').reset();
    document.getElementById('editLegislationId').value = '';
    document.getElementById('legislationFormTitle').textContent = "Yangi hujjat qo'shish";
    document.getElementById('legislationFormModal').classList.add('open');
}

function closeLegislationFormModal() {
    document.getElementById('legislationFormModal').classList.remove('open');
}

async function submitLegislationForm(e) {
    e.preventDefault();
    const id = document.getElementById('editLegislationId').value;
    const title = document.getElementById('legTitleInput').value.trim();
    const description = document.getElementById('legDescInput').value.trim();
    const category = document.getElementById('legCategoryInput').value;
    const fileUrl = document.getElementById('legFileUrlInput').value.trim();

    const payload = { title, description: description || null, category, file_url: fileUrl || null };
    const method = id ? 'PUT' : 'POST';
    const url = id ? `/api/legislations/${id}` : '/api/legislations/';

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            showToast("Hujjat muvaffaqiyatli saqlandi!", "success");
            closeLegislationFormModal();
            loadLegislationList();
        } else {
            showToast("Saqlashda xatolik yuz berdi.", "error");
        }
    } catch (error) {
        showToast("Server xatoligi.", "error");
    }
}

async function editLegislation(id) {
    try {
        const response = await fetch(`/api/legislations/${id}`);
        if (response.ok) {
            const leg = await response.json();
            document.getElementById('editLegislationId').value = leg.id;
            document.getElementById('legTitleInput').value = leg.title;
            document.getElementById('legDescInput').value = leg.description || '';
            document.getElementById('legCategoryInput').value = leg.category;
            document.getElementById('legFileUrlInput').value = leg.file_url || '';
            
            document.getElementById('legislationFormTitle').textContent = "Hujjatni tahrirlash";
            document.getElementById('legislationFormModal').classList.add('open');
        }
    } catch (e) {
        showToast("Ma'lumotlarni yuklab bo'lmadi.", "error");
    }
}

async function deleteLegislation(id) {
    if (!confirm("Ushbu hujjatni o'chirib tashlamoqchimisiz?")) return;

    try {
        const response = await fetch(`/api/legislations/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        if (response.ok) {
            showToast("Muvaffaqiyatli o'chirildi.", "success");
            loadLegislationList();
        } else {
            showToast("O'chirishda xatolik.", "error");
        }
    } catch (e) {
        showToast("Server xatoligi.", "error");
    }
}

/* ==========================================================================
   Applications (Feedbacks) Viewer
   ========================================================================== */
async function loadApplicationsList() {
    const tbody = document.getElementById('applicationsTableBody');
    tbody.innerHTML = '<tr><td colspan="5" style="text-align: center;">Yuklanmoqda...</td></tr>';

    try {
        const response = await fetch('/api/applications/', {
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        if (response.ok) {
            const list = await response.json();
            if (list.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--text-muted);">Murojaatlar mavjud emas.</td></tr>';
                return;
            }

            tbody.innerHTML = list.map(app => {
                let statusBadge = '';
                let actionBtn = '';

                if (app.status === 'Pending') {
                    statusBadge = `<span style="background-color: rgba(245,158,11,0.15); color: var(--color-accent); padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: 600;">Kutilmoqda</span>`;
                    actionBtn = `<button onclick="resolveApplication(${app.id})" class="btn btn-secondary" style="padding: 6px 12px; font-size: 0.75rem; background-color: var(--color-success); border-color: var(--color-success); color: white;">O'rganildi deb belgilash</button>`;
                } else {
                    statusBadge = `<span style="background-color: rgba(16,185,129,0.15); color: var(--color-success); padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: 600;">O'rganildi</span>`;
                }

                return `
                    <tr>
                        <td><strong>${escapeHTML(app.full_name)}</strong></td>
                        <td><a href="tel:${app.phone}" style="color: var(--color-primary);">${escapeHTML(app.phone)}</a></td>
                        <td style="max-width: 300px; white-space: pre-wrap; font-size: 0.9rem;">${escapeHTML(app.message)}</td>
                        <td>${statusBadge}</td>
                        <td style="text-align: right; display: flex; align-items: center; justify-content: flex-end; gap: 8px;">
                            ${actionBtn}
                            <button onclick="deleteApplication(${app.id})" class="admin-action-btn btn-delete" style="padding: 8px;">🗑️</button>
                        </td>
                    </tr>
                `;
            }).join('');
        }
    } catch (e) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--color-danger);">Yuklashda xatolik.</td></tr>';
    }
}

async function resolveApplication(id) {
    try {
        const response = await fetch(`/api/applications/${id}/status`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ status: 'Resolved' })
        });
        if (response.ok) {
            showToast("Murojaat holati yangilandi.", "success");
            loadApplicationsList();
        } else {
            showToast("O'zgartirishda xatolik.", "error");
        }
    } catch (e) {
        showToast("Server xatoligi.", "error");
    }
}

async function deleteApplication(id) {
    if (!confirm("Ushbu murojaatni o'chirib tashlamoqchimisiz?")) return;

    try {
        const response = await fetch(`/api/applications/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${authToken}` }
        });
        if (response.ok) {
            showToast("Murojaat o'chirildi.", "success");
            loadApplicationsList();
        } else {
            showToast("O'chirishda xatolik.", "error");
        }
    } catch (e) {
        showToast("Server xatoligi.", "error");
    }
}

/* ==========================================================================
   File Uploading Helper
   ========================================================================== */
function triggerFileInput(fileInputId) {
    document.getElementById(fileInputId).click();
}

async function handleFileUpload(fileInputId, targetInputId) {
    const fileInput = document.getElementById(fileInputId);
    const targetInput = document.getElementById(targetInputId);
    
    if (fileInput.files.length === 0) return;
    
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);
    
    showToast("Fayl yuklanmoqda...", "info");
    
    try {
        const response = await fetch('/api/upload/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${authToken}`
            },
            body: formData
        });
        
        if (response.ok) {
            const data = await response.json();
            targetInput.value = data.url;
            showToast("Fayl muvaffaqiyatli yuklandi!", "success");
        } else {
            const err = await response.json();
            showToast(err.detail || "Fayl yuklashda xatolik yuz berdi.", "error");
        }
    } catch (error) {
        console.error(error);
        showToast("Yuklash jarayonida xatolik yuz berdi.", "error");
    }
}

/* ==========================================================================
   Staff CRUD
   ========================================================================== */
async function loadStaffList() {
    const tbody = document.getElementById('staffTableBody');
    tbody.innerHTML = '<tr><td colspan="5" style="text-align: center;">Yuklanmoqda...</td></tr>';

    try {
        const response = await fetch('/api/staff/');
        if (response.ok) {
            const staffList = await response.json();
            if (staffList.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--text-muted);">Xodimlar ro\'yxati bo\'sh.</td></tr>';
                return;
            }

            tbody.innerHTML = staffList.map(member => {
                return `
                    <tr>
                        <td style="font-weight: 600; color: var(--color-primary);">${escapeHTML(member.full_name)}</td>
                        <td>${escapeHTML(member.position)}</td>
                        <td>${member.phone ? escapeHTML(member.phone) : '—'}</td>
                        <td>${member.email ? escapeHTML(member.email) : '—'}</td>
                        <td style="text-align: right; white-space: nowrap;">
                            <button onclick="editStaff(${member.id})" class="btn btn-secondary" style="padding: 4px 8px; font-size: 0.75rem; margin-right: 4px;">✏️ Tahrirlash</button>
                            <button onclick="deleteStaff(${member.id})" class="btn btn-secondary" style="padding: 4px 8px; font-size: 0.75rem; color: var(--color-danger); border-color: rgba(220,38,38,0.2);">❌ O'chirish</button>
                        </td>
                    </tr>
                `;
            }).join('');
        } else {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--color-danger);">Yuklashda xatolik yuz berdi.</td></tr>';
        }
    } catch (error) {
        console.error(error);
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--color-danger);">Server bilan aloqa uzildi.</td></tr>';
    }
}

function openStaffFormModal(member = null) {
    const modal = document.getElementById('staffFormModal');
    const title = document.getElementById('staffFormTitle');
    
    if (member) {
        title.textContent = "Xodim ma'lumotlarini tahrirlash";
        document.getElementById('editStaffId').value = member.id;
        document.getElementById('staffNameInput').value = member.full_name;
        document.getElementById('staffPositionInput').value = member.position;
        document.getElementById('staffPhoneInput').value = member.phone || '';
        document.getElementById('staffEmailInput').value = member.email || '';
    } else {
        title.textContent = "Yangi xodim qo'shish";
        document.getElementById('staffForm').reset();
        document.getElementById('editStaffId').value = '';
    }
    
    modal.classList.add('open');
}

function closeStaffFormModal() {
    document.getElementById('staffFormModal').classList.remove('open');
}

async function submitStaffForm(e) {
    e.preventDefault();
    const id = document.getElementById('editStaffId').value;
    const full_name = document.getElementById('staffNameInput').value.trim();
    const position = document.getElementById('staffPositionInput').value.trim();
    const phone = document.getElementById('staffPhoneInput').value.trim() || null;
    const email = document.getElementById('staffEmailInput').value.trim() || null;

    const submitBtn = e.target.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.innerHTML = 'Saqlanmoqda...';

    const payload = { full_name, position, phone, email };
    const url = id ? `/api/staff/${id}` : '/api/staff/';
    const method = id ? 'PUT' : 'POST';

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            showToast("Xodim ma'lumotlari muvaffaqiyatli saqlandi!", "success");
            closeStaffFormModal();
            loadStaffList();
        } else {
            const err = await response.json();
            showToast(err.detail || "Saqlashda xatolik yuz berdi.", "error");
        }
    } catch (error) {
        console.error(error);
        showToast("Serverga ulanib bo'lmadi.", "error");
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Saqlash';
    }
}

async function editStaff(id) {
    showToast("Ma'lumotlar yuklanmoqda...", "info");
    try {
        const response = await fetch(`/api/staff/${id}`);
        if (response.ok) {
            const member = await response.json();
            openStaffFormModal(member);
        } else {
            showToast("Xodim ma'lumotlarini yuklashda xatolik.", "error");
        }
    } catch (error) {
        console.error(error);
        showToast("Server bilan aloqa uzildi.", "error");
    }
}

async function deleteStaff(id) {
    if (!confirm("Haqiqatan ham ushbu xodimni ro'yxatdan o'chirmoqchimisiz?")) return;

    try {
        const response = await fetch(`/api/staff/${id}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (response.ok) {
            showToast("Xodim ro'yxatdan o'chirildi.", "success");
            loadStaffList();
        } else {
            showToast("O'chirishda xatolik yuz berdi.", "error");
        }
    } catch (error) {
        console.error(error);
        showToast("Server bilan aloqa uzildi.", "error");
    }
}
