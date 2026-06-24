import glob, re

bg_css = """<style id="bg-v3">
html {
  height: 100%;
}
body {
  min-height: 100vh;
  position: relative;
  background: #060810 !important;
}
body::before {
  content: '';
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  z-index: -1;
  background:
    radial-gradient(ellipse at 10% 10%, rgba(5,60,30,0.8) 0%, transparent 50%),
    radial-gradient(ellipse at 90% 90%, rgba(60,5,40,0.7) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 50%, rgba(10,10,35,0.9) 0%, transparent 70%),
    #060810;
}
.sidebar {
  background: rgba(4,7,5,0.98) !important;
  border-right: 1px solid rgba(34,197,94,0.1) !important;
}
.navbar {
  background: rgba(4,6,10,0.98) !important;
  backdrop-filter: blur(20px) !important;
}
.app-wrapper, .main-content, .content-area,
#sessionsView, #analyticsView,
.backtest-sessions {
  background: transparent !important;
}
.kpi-card, .card, .session-card, .chart-card,
.settings-card, .modal-box {
  background: rgba(12,15,20,0.88) !important;
  backdrop-filter: blur(8px) !important;
}
.chart-area { background: rgba(5,7,6,0.98) !important; }
.chart-topbar { background: rgba(4,6,5,0.98) !important; }
.balance-bar { background: rgba(4,6,5,0.95) !important; }
.trade-panel { background: rgba(5,7,6,0.98) !important; }
.panel-block { background: transparent !important; }
.quit-bar { background: rgba(4,6,5,0.98) !important; }
#chart-container { background: rgba(5,7,5,0.98) !important; }
input, select, textarea {
  background: rgba(8,10,14,0.9) !important;
}
</style>"""

html_files = glob.glob('frontend/*.html')
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    for old_id in ['bg-v3', 'bg-v2', 'bg-global', 'bg-fix']:
        c = re.sub(r'<style id="' + old_id + r'">.*?</style>', '', c, flags=re.DOTALL)
    c = c.replace('</head>', bg_css + '</head>')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(filepath + ' done!')