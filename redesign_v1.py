# Nouveau global.css complet
css = """
:root {
  --bg-primary: #0a0a0a;
  --bg-card: #141618;
  --bg-card-2: #1a1e24;
  --bg-sidebar: #141618;
  --accent: #3ddc68;
  --accent-dim: rgba(61,220,104,0.12);
  --accent-border: rgba(61,220,104,0.3);
  --text-primary: #ffffff;
  --text-secondary: #6b7280;
  --text-muted: #374151;
  --border: #1f2937;
  --green: #3ddc68;
  --red: #ef4444;
  --blue: #3b82f6;
  --purple: #8b5cf6;
  --gold: #f59e0b;
  --sidebar-width: 200px;
  --right-panel-width: 280px;
  --navbar-height: 56px;
  --radius: 12px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', -apple-system, sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 14px;
  line-height: 1.5;
}

/* SCROLLBAR */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 2px; }

/* APP LAYOUT */
.app-container {
  display: flex;
  min-height: 100vh;
}

/* SIDEBAR */
.sidebar {
  width: var(--sidebar-width);
  min-width: var(--sidebar-width);
  height: 100vh;
  position: fixed;
  left: 0; top: 0;
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  z-index: 100;
  overflow-y: auto;
}

.sidebar-header {
  padding: 20px 16px;
  border-bottom: 1px solid var(--border);
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.logo-icon {
  width: 32px; height: 32px;
  background: var(--accent);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
}

.logo-name {
  font-size: 14px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.sidebar-search {
  width: 100%;
  background: var(--bg-card-2);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 8px 12px;
  color: var(--text-secondary);
  font-size: 12px;
  font-family: Inter, sans-serif;
  outline: none;
}

.sidebar-search:focus { border-color: var(--accent-border); }

.nav-section {
  padding: 16px 12px 4px;
}

.nav-section-label {
  font-size: 10px;
  font-weight: 600;
  color: var(--text-muted);
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 0 4px;
  margin-bottom: 4px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.15s;
  cursor: pointer;
  margin-bottom: 2px;
  border: none;
  background: transparent;
  width: 100%;
  text-align: left;
}

.nav-item svg {
  width: 16px; height: 16px;
  flex-shrink: 0;
  stroke: currentColor;
}

.nav-item:hover {
  background: var(--bg-card-2);
  color: var(--text-primary);
}

.nav-item.active {
  background: var(--accent) !important;
  color: #000 !important;
  font-weight: 600;
}

.nav-item.active svg { stroke: #000; }

.sidebar-footer {
  margin-top: auto;
  padding: 12px;
  border-top: 1px solid var(--border);
}

/* MAIN CONTENT */
.main-content {
  margin-left: var(--sidebar-width);
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

/* NAVBAR */
.navbar {
  height: var(--navbar-height);
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border);
  background: var(--bg-primary);
  position: sticky;
  top: 0;
  z-index: 50;
}

.navbar-left {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.breadcrumb {
  font-size: 11px;
  color: var(--text-muted);
}

.page-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.navbar-icon-btn {
  width: 34px; height: 34px;
  border-radius: 8px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  color: var(--text-secondary);
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  transition: all 0.15s;
}

.navbar-icon-btn:hover {
  border-color: var(--accent-border);
  color: var(--text-primary);
}

.navbar-icon-btn svg { width: 15px; height: 15px; }

.period-pill {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.period-pill:hover { border-color: var(--accent-border); color: var(--text-primary); }

.avatar-btn {
  width: 32px; height: 32px;
  border-radius: 50%;
  background: var(--accent-dim);
  border: 2px solid var(--accent-border);
  color: var(--accent);
  font-size: 12px;
  font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  overflow: hidden;
}

.avatar-btn img { width: 100%; height: 100%; object-fit: cover; }

/* CONTENT AREA */
.content-area {
  padding: 20px 24px;
  flex: 1;
}

/* KPI GRID */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.kpi-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px 20px;
  transition: all 0.2s;
}

.kpi-card:hover {
  border-color: #2a2a2a;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.3);
}

.kpi-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 10px;
}

.kpi-value {
  font-size: 28px;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.03em;
  line-height: 1;
  margin-bottom: 8px;
}

.kpi-value.empty { color: var(--text-muted); }

.kpi-change {
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.kpi-change.up { color: var(--green); }
.kpi-change.down { color: var(--red); }
.kpi-change.neutral { color: var(--text-secondary); }

/* DASHBOARD GRID */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr var(--right-panel-width);
  gap: 16px;
}

.dashboard-main { min-width: 0; }
.dashboard-right { min-width: 0; }

/* CARDS */
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
  margin-bottom: 16px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
}

.card-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
}

.card-body { padding: 20px; }

/* SECTION TITLE */
.section-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 12px;
}

/* BADGES */
.badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 8px;
  border-radius: 5px;
  font-size: 11px;
  font-weight: 600;
}

.badge-buy { background: rgba(61,220,104,0.12); color: #3ddc68; border: 1px solid rgba(61,220,104,0.2); }
.badge-sell { background: rgba(239,68,68,0.12); color: #ef4444; border: 1px solid rgba(239,68,68,0.2); }
.badge-win { background: rgba(61,220,104,0.12); color: #3ddc68; border: 1px solid rgba(61,220,104,0.2); }
.badge-loss { background: rgba(239,68,68,0.12); color: #ef4444; border: 1px solid rgba(239,68,68,0.2); }
.badge-be { background: rgba(245,158,11,0.12); color: #f59e0b; border: 1px solid rgba(245,158,11,0.2); }

/* TABLES */
.data-table { width: 100%; border-collapse: collapse; }
.data-table th {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 10px 16px;
  text-align: left;
  border-bottom: 1px solid var(--border);
}
.data-table td {
  padding: 12px 16px;
  font-size: 13px;
  border-bottom: 1px solid #0f0f0f;
}
.data-table tr:hover td { background: #0f0f0f; }

/* INPUTS */
input, select, textarea {
  background: var(--bg-card-2);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text-primary);
  font-family: Inter, sans-serif;
  font-size: 13px;
  padding: 10px 12px;
  outline: none;
  transition: border-color 0.15s;
  width: 100%;
}
input:focus, select:focus, textarea:focus { border-color: var(--accent-border); }
select option { background: var(--bg-card-2); }

/* BUTTONS */
.btn-primary {
  display: flex; align-items: center; gap: 6px;
  padding: 8px 16px;
  background: var(--accent);
  color: #000;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  white-space: nowrap;
  font-family: Inter, sans-serif;
}
.btn-primary:hover { background: #2bc45a; }
.btn-primary svg { width: 14px; height: 14px; }

.btn-secondary {
  padding: 8px 16px;
  background: var(--bg-card-2);
  color: var(--text-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 13px;
  cursor: pointer;
  font-family: Inter, sans-serif;
}
.btn-secondary:hover { color: var(--text-primary); border-color: #2a2a2a; }

/* NOTIFICATION PANEL */
.notif-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
}
.notif-item:last-child { border: none; }
.notif-avatar {
  width: 32px; height: 32px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}
.notif-text { font-size: 12px; color: var(--text-primary); line-height: 1.4; }
.notif-time { font-size: 11px; color: var(--text-muted); margin-top: 2px; }

/* ACTIVITY ITEM */
.activity-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
  border-bottom: 1px solid var(--border);
  font-size: 12px;
}
.activity-item:last-child { border: none; }
.activity-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

/* MODAL */
.modal {
  display: none;
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.7);
  backdrop-filter: blur(4px);
  z-index: 1000;
  align-items: center; justify-content: center;
}
.modal.active { display: flex; }
.modal-box {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 28px;
  width: 90%;
  max-width: 560px;
  max-height: 90vh;
  overflow-y: auto;
}
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}
.modal-title { font-size: 16px; font-weight: 700; }

/* EMPTY STATE */
.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: var(--text-secondary);
}
.empty-state-icon { font-size: 40px; margin-bottom: 12px; }
.empty-state-title { font-size: 15px; font-weight: 500; margin-bottom: 6px; }
.empty-state-sub { font-size: 13px; color: var(--text-muted); }

/* LOGOUT BTN */
.logout-btn {
  display: flex; align-items: center; gap: 8px;
  padding: 9px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  color: var(--red);
  background: transparent;
  border: none;
  cursor: pointer;
  width: 100%;
  font-family: Inter, sans-serif;
  transition: all 0.15s;
}
.logout-btn:hover { background: rgba(239,68,68,0.08); }

/* TOAST */
.toast {
  position: fixed;
  bottom: 24px; right: 24px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 12px 16px;
  font-size: 13px;
  z-index: 9999;
  transform: translateY(80px);
  opacity: 0;
  transition: all 0.3s;
}
.toast.show { transform: translateY(0); opacity: 1; }
.toast.success { border-color: rgba(61,220,104,0.4); }
.toast.error { border-color: rgba(239,68,68,0.4); }

/* RANGE */
input[type=range] {
  -webkit-appearance: none;
  height: 4px;
  border-radius: 2px;
  background: var(--border);
  padding: 0;
}
input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px; height: 16px;
  border-radius: 50%;
  background: var(--accent);
  cursor: pointer;
  border: 2px solid var(--bg-primary);
}

/* RESPONSIVE */
@media (max-width: 1400px) {
  .dashboard-grid { grid-template-columns: 1fr; }
  .dashboard-right { display: none; }
}
@media (max-width: 1024px) {
  .kpi-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .sidebar { transform: translateX(-100%); transition: transform 0.3s; }
  .sidebar.open { transform: translateX(0); }
  .main-content { margin-left: 0; }
  .kpi-grid { grid-template-columns: 1fr 1fr; }
}
"""

with open('frontend/css/global.css', 'w', encoding='utf-8') as f:
    f.write(css)
print('global.css rewritten!')