layout_js = """
const BASE_URL = window.location.hostname === 'localhost'
  ? 'http://localhost:8001'
  : 'https://smartreview-y4sq.onrender.com';

const NAV_ITEMS = [
  { section: 'DASHBOARDS', items: [
    { href: 'index.html', icon: 'layout-dashboard', label: 'Overview' },
    { href: 'journal.html', icon: 'book-open', label: 'Journal' },
    { href: 'calendar.html', icon: 'calendar', label: 'Calendrier' },
    { href: 'stats.html', icon: 'bar-chart-2', label: 'Statistiques' },
    { href: 'coach.html', icon: 'brain', label: 'IA Coach' },
    { href: 'accounts.html', icon: 'wallet', label: 'Comptes' },
  ]},
  { section: 'OUTILS', items: [
    { href: 'notes.html', icon: 'file-text', label: 'Notes & Projets' },
    { href: 'backtesting.html', icon: 'activity', label: 'Backtesting' },
    { href: 'strategy-builder.html', icon: 'layers', label: 'Strategy Builder' },
    { href: 'copy-trading.html', icon: 'copy', label: 'Copy Trading' },
  ]},
  { section: 'COMMUNAUTÉ', items: [
    { href: 'marketplace.html', icon: 'shopping-bag', label: 'Marketplace' },
    { href: 'community.html', icon: 'users', label: 'Communauté' },
    { href: 'podcasts.html', icon: 'headphones', label: 'Podcasts' },
    { href: 'live.html', icon: 'radio', label: 'Live Direct' },
  ]},
  { section: 'SETTINGS', items: [
    { href: 'settings.html', icon: 'settings', label: 'Paramètres' },
    { href: 'help.html', icon: 'help-circle', label: 'Aide' },
  ]},
];

function getCurrentPage() {
  return window.location.pathname.split('/').pop() || 'index.html';
}

function buildSidebar() {
  const current = getCurrentPage();
  const sections = NAV_ITEMS.map(s => `
    <div class="nav-section">
      <div class="nav-section-label">${s.section}</div>
      ${s.items.map(item => `
        <a href="/${item.href}" class="nav-item ${current === item.href ? 'active' : ''}">
          <i data-lucide="${item.icon}"></i>
          <span>${item.label}</span>
        </a>
      `).join('')}
    </div>
  `).join('');

  return `
    <aside class="sidebar" id="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <div class="logo-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="2.5">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
            </svg>
          </div>
          <span class="logo-name">SmartFX-Review</span>
        </div>
        <input type="text" class="sidebar-search" placeholder="Search...">
      </div>
      ${sections}
      <div class="sidebar-footer">
        <div class="account-selector-label">Compte Actif</div>
        <select id="activeAccount" style="width:100%;font-size:12px;margin-bottom:8px;padding:6px 8px;background:#1a1e24;border:1px solid #1f2937;border-radius:6px;color:#fff;">
          <option>Aucun compte</option>
        </select>
        <div style="display:flex;align-items:center;gap:6px;font-size:11px;color:#6b7280;">
          <span id="backendStatus" style="width:7px;height:7px;border-radius:50%;background:#3ddc68;display:inline-block;animation:pulse 2s infinite;"></span>
          <span id="backendStatusText">Vérification...</span>
        </div>
      </div>
    </aside>`;
}

function buildNavbar(title, breadcrumb) {
  let user = {};
  try { user = JSON.parse(localStorage.getItem('user') || '{}'); } catch(e) {}
  const avatar = user.picture 
    ? `<img src="${user.picture}" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">`
    : (user.name ? user.name.slice(0,2).toUpperCase() : 'TR');

  return `
    <nav class="navbar">
      <div class="navbar-left">
        <span class="breadcrumb">${breadcrumb || 'Dashboards / ' + title}</span>
        <h1 class="page-title">${title}</h1>
      </div>
      <div class="navbar-right">
        <div class="period-pill">Today ▾</div>
        <button class="navbar-icon-btn" onclick="location.reload()" title="Refresh">
          <i data-lucide="refresh-cw"></i>
        </button>
        <button class="navbar-icon-btn" id="notifBtn" title="Notifications">
          <i data-lucide="bell"></i>
        </button>
        <div class="avatar-btn" id="userAvatar">${avatar}</div>
      </div>
    </nav>`;
}

function initLayout(title, breadcrumb) {
  // Inject CSS variables if not present
  if(!document.getElementById('layout-css')) {
    const style = document.createElement('style');
    style.id = 'layout-css';
    style.textContent = `
      @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
      .sidebar { position:fixed;left:0;top:0;width:200px;height:100vh;background:#141618;border-right:1px solid #1f2937;display:flex;flex-direction:column;z-index:100;overflow-y:auto; }
      .sidebar-header { padding:16px;border-bottom:1px solid #1f2937; }
      .logo { display:flex;align-items:center;gap:8px;margin-bottom:12px; }
      .logo-icon { width:30px;height:30px;background:#3ddc68;border-radius:8px;display:flex;align-items:center;justify-content:center; }
      .logo-name { font-size:13px;font-weight:700;color:#fff; }
      .sidebar-search { width:100%;background:#1a1e24;border:1px solid #1f2937;border-radius:7px;padding:7px 10px;color:#9ca3af;font-size:12px;font-family:Inter,sans-serif;outline:none; }
      .nav-section { padding:12px 10px 4px; }
      .nav-section-label { font-size:10px;font-weight:600;color:#374151;letter-spacing:0.1em;text-transform:uppercase;padding:0 4px;margin-bottom:4px; }
      .nav-item { display:flex;align-items:center;gap:8px;padding:7px 10px;border-radius:7px;font-size:12px;font-weight:500;color:#6b7280;text-decoration:none;transition:all 0.15s;margin-bottom:1px;border:none;background:transparent;width:100%;text-align:left;cursor:pointer; }
      .nav-item svg { width:15px;height:15px;flex-shrink:0;stroke:currentColor; }
      .nav-item:hover { background:#1a1e24;color:#fff; }
      .nav-item.active { background:#3ddc68!important;color:#000!important;font-weight:600; }
      .nav-item.active svg { stroke:#000; }
      .sidebar-footer { margin-top:auto;padding:12px;border-top:1px solid #1f2937; }
      .account-selector-label { font-size:10px;color:#374151;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px; }
      .navbar { height:52px;padding:0 20px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #1f2937;background:#0a0a0a;position:sticky;top:0;z-index:50; }
      .navbar-left { display:flex;flex-direction:column;gap:1px; }
      .breadcrumb { font-size:11px;color:#374151; }
      .page-title { font-size:17px;font-weight:700;color:#fff;letter-spacing:-0.02em; }
      .navbar-right { display:flex;align-items:center;gap:7px; }
      .navbar-icon-btn { width:32px;height:32px;border-radius:7px;background:#141618;border:1px solid #1f2937;color:#6b7280;display:flex;align-items:center;justify-content:center;cursor:pointer;transition:all 0.15s; }
      .navbar-icon-btn:hover { border-color:rgba(61,220,104,0.3);color:#fff; }
      .navbar-icon-btn svg { width:14px;height:14px; }
      .period-pill { background:#141618;border:1px solid #1f2937;border-radius:7px;padding:5px 10px;font-size:11px;font-weight:500;color:#6b7280;cursor:pointer;display:flex;align-items:center;gap:4px; }
      .avatar-btn { width:30px;height:30px;border-radius:50%;background:rgba(61,220,104,0.12);border:2px solid rgba(61,220,104,0.3);color:#3ddc68;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;cursor:pointer;overflow:hidden; }
      .main-content { margin-left:200px;display:flex;flex-direction:column;min-height:100vh; }
      .content-area { padding:20px 24px;flex:1; }
    `;
    document.head.appendChild(style);
  }

  // Build layout
  const root = document.getElementById('app-layout-root');
  if(root) {
    root.innerHTML = buildSidebar() + `<div class="main-content"><div id="navbar-placeholder"></div><div id="content-slot"></div></div>`;
    document.getElementById('navbar-placeholder').outerHTML = buildNavbar(title, breadcrumb);
  } else {
    // Inject sidebar before main content
    const existing = document.querySelector('.main-content, main, .app-wrapper');
    if(existing && !document.querySelector('.sidebar')) {
      const sidebarEl = document.createElement('div');
      sidebarEl.innerHTML = buildSidebar();
      document.body.insertBefore(sidebarEl.firstChild, document.body.firstChild);
      existing.style.marginLeft = '200px';
    }
  }

  // Load accounts
  loadAccountsIntoSelector('activeAccount');

  // Check backend
  checkBackend();

  // User avatar
  try {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    const el = document.getElementById('userAvatar');
    if(el && user.picture) {
      el.innerHTML = `<img src="${user.picture}" style="width:100%;height:100%;object-fit:cover;border-radius:50%;">`;
    } else if(el && user.name) {
      el.textContent = user.name.slice(0,2).toUpperCase();
    }
  } catch(e) {}

  // Logout
  document.addEventListener('click', function(e) {
    if(e.target.closest('#logoutBtn')) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login.html';
    }
  });

  // Init icons
  if(typeof lucide !== 'undefined') lucide.createIcons();
  else {
    const s = document.createElement('script');
    s.src = 'https://unpkg.com/lucide@latest';
    s.onload = () => lucide.createIcons();
    document.head.appendChild(s);
  }
}

async function checkBackend() {
  try {
    const r = await fetch(BASE_URL + '/');
    const dot = document.getElementById('backendStatus');
    const txt = document.getElementById('backendStatusText');
    if(r.ok) {
      if(dot) dot.style.background = '#3ddc68';
      if(txt) txt.textContent = 'En ligne';
    } else throw new Error();
  } catch {
    const dot = document.getElementById('backendStatus');
    const txt = document.getElementById('backendStatusText');
    if(dot) dot.style.background = '#ef4444';
    if(txt) txt.textContent = 'Hors ligne';
  }
}

async function loadAccountsIntoSelector(id) {
  try {
    const r = await fetch(BASE_URL + '/api/accounts/');
    const accounts = await r.json();
    const sel = document.getElementById(id);
    if(sel && accounts && accounts.length > 0) {
      sel.innerHTML = accounts.map(a => `<option value="${a.id}">${a.name}</option>`).join('');
    }
  } catch(e) {}
}

async function initializeCommon() {
  checkBackend();
  await loadAccountsIntoSelector('activeAccount');
  setInterval(checkBackend, 10 * 60 * 1000);
}

// Auto-init
document.addEventListener('DOMContentLoaded', function() {
  if(typeof lucide !== 'undefined') lucide.createIcons();
  initializeCommon();
});
"""

with open('frontend/js/layout.js', 'w', encoding='utf-8') as f:
    f.write(layout_js)
print('layout.js rewritten!')