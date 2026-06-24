/**
 * SmartFX-Review — Shared layout (navbar + collapsible sidebar)
 */

const NAVBAR_LINKS = [
    { href: 'index.html', label: 'Overview' },
    { href: 'journal.html', label: 'Journal' },
    { href: 'calendar.html', label: 'Calendrier' },
    { href: 'stats.html', label: 'Statistiques' },
    { href: 'coach.html', label: 'IA Coach' },
    { href: 'accounts.html', label: 'Comptes' },
];

const SIDEBAR_TOOLS = [
    { href: 'notes.html', icon: 'file-text', label: 'Notes & Projets' },
    { href: 'backtesting.html', icon: 'activity', label: 'Backtesting' },
    { href: 'strategy-builder.html', icon: 'layers', label: 'Strategy Builder' },
    { href: 'copy-trading.html', icon: 'copy', label: 'Copy Trading' },
];

const SIDEBAR_COMMUNITY = [
    { href: 'marketplace.html', icon: 'shopping-bag', label: 'Marketplace' },
    { href: 'community.html', icon: 'users', label: 'Communauté' },
    { href: 'podcasts.html', icon: 'headphones', label: 'Podcasts' },
    { href: 'live.html', icon: 'radio', label: 'Live Direct' },
];

const SIDEBAR_SETTINGS = [
    { href: 'settings.html', icon: 'settings', label: 'Paramètres' },
    { href: 'help.html', icon: 'help-circle', label: 'Aide' },
];

function getCurrentPage() {
    const path = window.location.pathname;
    const file = path.split('/').pop() || 'index.html';
    return file === '' ? 'index.html' : file;
}

function sidebarItem(href, icon, label, current) {
    const active = current === href ? 'active' : '';
    return `<a href="${href}" class="sidebar-item ${active}"><i data-lucide="${icon}"></i><span>${label}</span></a>`;
}

function buildNavbar(current) {
    const links = NAVBAR_LINKS.map(({ href, label }) => {
        const active = current === href ? 'active' : '';
        return `<a href="${href}" class="navbar-link ${active}">${label}</a>`;
    }).join('');

    return `
    <nav class="navbar">
        <a href="index.html" class="navbar-logo">
            <svg width="28" height="28" viewBox="0 0 32 32" fill="none" aria-hidden="true">
                <rect width="32" height="32" rx="10" fill="#22C55E"/>
                <polyline points="6,22 12,14 17,18 22,10 26,10" stroke="#000" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
                <circle cx="26" cy="10" r="2.5" fill="#000"/>
            </svg>
            <span class="navbar-logo-text">SmartFX-Review</span>
        </a>
        <div class="navbar-nav">${links}</div>
        <div class="navbar-right">
            <div class="balance-pill" id="balancePill" title="Solde total">
                Solde <span id="totalBalance">--</span>
            </div>
            <div class="navbar-search-wrap">
                <i data-lucide="search" class="navbar-search-icon"></i>
                <input type="text" class="navbar-search-input" placeholder="Rechercher..." id="globalSearch">
            </div>
            <button class="btn-icon" id="notifBtn" type="button" title="Notifications">
                <i data-lucide="bell"></i>
            </button>
            <button class="btn-icon mobile-menu-btn" id="mobileMenuBtn" type="button" title="Menu">
                <i data-lucide="menu"></i>
            </button>
            <div class="user-menu-wrap">
                <button class="user-avatar-btn" id="userAvatarBtn" type="button" aria-label="Menu utilisateur">
                    <img class="user-avatar-img hidden" id="userAvatarImg" alt="" width="32" height="32">
                    <span class="user-avatar-initials" id="userAvatarInitials">TR</span>
                </button>
                <div class="user-dropdown" id="userDropdown">
                    <a href="settings.html" class="user-dropdown-item"><i data-lucide="user"></i><span>Profil</span></a>
                    <a href="settings.html" class="user-dropdown-item"><i data-lucide="settings"></i><span>Paramètres</span></a>
                    <button type="button" class="user-dropdown-item danger" id="logoutBtn"><i data-lucide="log-out"></i><span>Déconnexion</span></button>
                </div>
            </div>
        </div>
    </nav>`;
}

function buildSidebar(current) {
    const tools = SIDEBAR_TOOLS.map(i => sidebarItem(i.href, i.icon, i.label, current)).join('');
    const community = SIDEBAR_COMMUNITY.map(i => sidebarItem(i.href, i.icon, i.label, current)).join('');
    const settings = SIDEBAR_SETTINGS.map(i => sidebarItem(i.href, i.icon, i.label, current)).join('');

    return `
    <div class="sidebar-overlay" id="sidebarOverlay"></div>
    <aside class="sidebar" id="sidebar">
        <button class="sidebar-toggle" id="sidebarToggle" type="button" aria-label="Réduire la sidebar">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
        </button>
        <button class="new-trade-btn" id="sidebarNewTradeBtn" type="button">
            <i data-lucide="plus"></i>
            <span>Nouveau Trade</span>
        </button>
        <div class="sidebar-section-label">OUTILS</div>
        ${tools}
        <div class="sidebar-section-label">COMMUNAUTÉ</div>
        ${community}
        <div class="sidebar-section-label">SETTINGS</div>
        ${settings}
        <div class="sidebar-footer">
            <label class="account-selector-label" for="activeAccount">Compte Actif</label>
            <select id="activeAccount" class="select-input">
                <option value="">Chargement...</option>
            </select>
            <div class="backend-status">
                <span class="status-dot" id="backendStatus"></span>
                <span class="status-text" id="backendStatusText">Vérification...</span>
            </div>
        </div>
    </aside>`;
}

function initSidebarToggle() {
    const sidebar = document.getElementById('sidebar');
    const appWrapper = document.getElementById('appWrapper');
    const toggle = document.getElementById('sidebarToggle');
    if (!sidebar || !appWrapper || !toggle) return;

    toggle.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
        appWrapper.classList.toggle('sidebar-collapsed');
        localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
    });

    if (localStorage.getItem('sidebarCollapsed') === 'true') {
        sidebar.classList.add('collapsed');
        appWrapper.classList.add('sidebar-collapsed');
    }
}

function initMobileDrawer() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    const menuBtn = document.getElementById('mobileMenuBtn');
    if (!sidebar || !overlay || !menuBtn) return;

    const open = () => {
        sidebar.classList.add('mobile-open');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    };

    const close = () => {
        sidebar.classList.remove('mobile-open');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    };

    menuBtn.addEventListener('click', () => {
        if (sidebar.classList.contains('mobile-open')) close();
        else open();
    });
    overlay.addEventListener('click', close);

    document.querySelectorAll('.sidebar-item').forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 768) close();
        });
    });
}

function initUserMenu() {
    const btn = document.getElementById('userAvatarBtn');
    const dropdown = document.getElementById('userDropdown');
    if (!btn || !dropdown) return;

    btn.addEventListener('click', (e) => {
        e.stopPropagation();
        dropdown.classList.toggle('open');
    });

    document.addEventListener('click', () => dropdown.classList.remove('open'));

    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            if (typeof logout === 'function') logout();
        });
    }
}

function initUserAvatar() {
    const img = document.getElementById('userAvatarImg');
    const initials = document.getElementById('userAvatarInitials');
    if (!img || !initials) return;

    try {
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        if (user.picture) {
            img.src = user.picture;
            img.alt = user.name || 'Avatar';
            img.classList.remove('hidden');
            initials.classList.add('hidden');
        } else if (user.name || user.email) {
            const source = user.name || user.email;
            initials.textContent = source.slice(0, 2).toUpperCase();
        }
    } catch (_) {
        /* keep default initials */
    }
}

async function loadBalancePill() {
    const el = document.getElementById('totalBalance');
    if (!el || typeof API === 'undefined') return;

    try {
        const accounts = await API.getAccounts();
        const total = accounts.reduce((sum, a) => sum + (a.current_balance || 0), 0);
        el.textContent = typeof formatCurrency === 'function' ? formatCurrency(total) : `$${total.toFixed(2)}`;
    } catch (_) {
        el.textContent = '--';
    }
}

function initNewTradeButton() {
    const sidebarBtn = document.getElementById('sidebarNewTradeBtn');
    if (!sidebarBtn) return;

    sidebarBtn.addEventListener('click', () => {
        const pageBtn = document.getElementById('newTradeBtn');
        if (pageBtn) {
            pageBtn.click();
            return;
        }
        const modal = document.getElementById('tradeModal');
        if (modal) {
            const form = document.getElementById('tradeForm');
            if (form) form.reset();
            modal.classList.add('active');
            return;
        }
        window.location.href = 'journal.html';
    });
}

function initLayout() {
    const current = getCurrentPage();
    const placeholder = document.getElementById('app-layout-root');
    if (!placeholder) return;

    placeholder.innerHTML = buildNavbar(current) + buildSidebar(current);

    if (typeof lucide !== 'undefined') lucide.createIcons();

    initSidebarToggle();
    initMobileDrawer();
    initUserMenu();
    initUserAvatar();
    initNewTradeButton();
    loadBalancePill();

    if (typeof initializeCommon === 'function') {
        initializeCommon();
    }

    document.dispatchEvent(new CustomEvent('layout-ready'));
}

document.addEventListener('DOMContentLoaded', initLayout);
