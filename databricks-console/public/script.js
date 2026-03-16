// ===========================
// Greeting
// ===========================
function setGreeting() {
    const hour = new Date().getHours();
    let greeting = 'Good evening';
    if (hour < 12) greeting = 'Good morning';
    else if (hour < 17) greeting = 'Good afternoon';
    const el = document.getElementById('greeting');
    if (el) el.textContent = `${greeting}, John`;
}

setGreeting();

// ===========================
// Theme Toggle
// ===========================
const themeToggle = document.querySelector('.theme-toggle');
const body = document.body;

const savedTheme = localStorage.getItem('theme') || 'light';
if (savedTheme === 'dark') {
    body.setAttribute('data-theme', 'dark');
    themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
}

themeToggle.addEventListener('click', () => {
    const isDark = body.getAttribute('data-theme') === 'dark';
    body.setAttribute('data-theme', isDark ? 'light' : 'dark');
    localStorage.setItem('theme', isDark ? 'light' : 'dark');
    themeToggle.innerHTML = `<i class="fas fa-${isDark ? 'moon' : 'sun'}"></i>`;
});

// ===========================
// Sidebar Toggle
// ===========================
const sidebar = document.getElementById('sidebar');
const mainContent = document.getElementById('mainContent');
const navLeft = document.querySelector('.nav-left');
const sidebarToggle = document.getElementById('sidebarToggle');
const overlay = document.getElementById('sidebarOverlay');

function isMobile() {
    return window.innerWidth <= 768;
}

// Restore collapsed state on desktop
if (!isMobile() && localStorage.getItem('sidebarCollapsed') === 'true') {
    sidebar.classList.add('collapsed');
    mainContent.classList.add('sidebar-collapsed');
    navLeft.classList.add('collapsed');
}

sidebarToggle.addEventListener('click', () => {
    if (isMobile()) {
        sidebar.classList.toggle('mobile-open');
        overlay.classList.toggle('active');
        return;
    }
    const isCollapsed = sidebar.classList.toggle('collapsed');
    mainContent.classList.toggle('sidebar-collapsed', isCollapsed);
    navLeft.classList.toggle('collapsed', isCollapsed);
    localStorage.setItem('sidebarCollapsed', isCollapsed);
});

overlay.addEventListener('click', () => {
    sidebar.classList.remove('mobile-open');
    overlay.classList.remove('active');
});

// Close mobile sidebar when a nav item is clicked
document.querySelectorAll('.sidebar-item').forEach(item => {
    item.addEventListener('click', e => {
        e.preventDefault();
        document.querySelectorAll('.sidebar-item').forEach(i => i.classList.remove('active'));
        item.classList.add('active');
        if (isMobile()) {
            sidebar.classList.remove('mobile-open');
            overlay.classList.remove('active');
        }
    });
});

// ===========================
// Action Handlers (global for inline onclick)
// ===========================
function handleAction(name) {
    showToast(`${name} initiated`, 'success');
}

function handleClusterAction(btn, action) {
    const item = btn.closest('.cluster-item');
    const name = item.querySelector('.cluster-name').textContent;
    const dot = item.querySelector('.cluster-dot');
    const actionsDiv = item.querySelector('.cluster-actions');

    showToast(`${action}: ${name}`, 'success');

    setTimeout(() => {
        if (action === 'Start') {
            dot.className = 'cluster-dot running';
            actionsDiv.innerHTML = `
                <button class="btn-ghost-sm" onclick="handleAction('Configure ${name}')">Configure</button>
                <button class="btn-danger-sm" onclick="handleClusterAction(this, 'Terminate')">Terminate</button>
            `;
        } else if (action === 'Terminate') {
            dot.className = 'cluster-dot stopped';
            actionsDiv.innerHTML = `
                <button class="btn-primary-sm" onclick="handleClusterAction(this, 'Start')">Start</button>
                <button class="btn-ghost-sm" onclick="handleAction('Configure ${name}')">Configure</button>
            `;
        }
    }, 700);
}

// ===========================
// Toast Notifications
// ===========================
const toastStyles = document.createElement('style');
toastStyles.textContent = `
    @keyframes toastIn  { from { transform: translateY(50px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
    @keyframes toastOut { from { transform: translateY(0); opacity: 1; } to { transform: translateY(50px); opacity: 0; } }
`;
document.head.appendChild(toastStyles);

function showToast(message, type = 'info') {
    const existing = document.querySelector('.toast-notification');
    if (existing) existing.remove();

    const colors = {
        success: '#22c55e',
        info: '#6366f1',
        warning: '#f59e0b',
        error: '#ef4444',
    };
    const icons = {
        success: 'check-circle',
        info: 'info-circle',
        warning: 'exclamation-circle',
        error: 'times-circle',
    };

    const toast = document.createElement('div');
    toast.className = 'toast-notification';
    toast.innerHTML = `<i class="fas fa-${icons[type] || 'info-circle'}"></i><span>${message}</span>`;
    toast.style.cssText = `
        position: fixed;
        bottom: 24px;
        right: 24px;
        background: ${colors[type] || colors.info};
        color: #ffffff;
        padding: 10px 16px;
        border-radius: 8px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.18);
        display: flex;
        align-items: center;
        gap: 9px;
        z-index: 9999;
        font-size: 13.5px;
        font-weight: 500;
        animation: toastIn 0.22s ease;
        font-family: inherit;
    `;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'toastOut 0.22s ease forwards';
        setTimeout(() => toast.remove(), 220);
    }, 2600);
}

// ===========================
// Search
// ===========================
const searchInput = document.querySelector('.search-bar input');

searchInput.addEventListener('keydown', e => {
    if (e.key === 'Enter' && e.target.value.trim()) {
        showToast(`Searching: ${e.target.value.trim()}`, 'info');
    }
    if (e.key === 'Escape') {
        e.target.value = '';
        e.target.blur();
    }
});

// ===========================
// Nav Icon Buttons
// ===========================
document.querySelectorAll('.nav-icon-btn:not(.theme-toggle):not(#sidebarToggle)').forEach(btn => {
    btn.addEventListener('click', () => {
        const title = btn.getAttribute('title');
        if (title) showToast(`${title} opened`, 'info');
    });
});

document.querySelector('.user-avatar').addEventListener('click', () => {
    showToast('Profile menu opened', 'info');
});

// ===========================
// Keyboard Shortcuts
// ===========================
document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        searchInput.focus();
        searchInput.select();
    }
    if ((e.ctrlKey || e.metaKey) && e.key === 'b') {
        e.preventDefault();
        sidebarToggle.click();
    }
});
