import glob, re

bg_css = """<style id="bg-global">
html {
  min-height: 100%;
  background: radial-gradient(ellipse at top left, #051a0f 0%, #0a0a1a 45%, #1a0812 100%) fixed !important;
}
body {
  min-height: 100vh;
  background: transparent !important;
}
.app-wrapper, .main-content, .content-area,
.backtest-sessions, .analytics-view,
#sessionsView, #analyticsView {
  background: transparent !important;
}
.sidebar {
  background: rgba(5,8,6,0.97) !important;
  border-right: 1px solid rgba(34,197,94,0.08) !important;
}
.navbar {
  background: rgba(5,8,12,0.97) !important;
  backdrop-filter: blur(20px) !important;
  border-bottom: 1px solid rgba(34,197,94,0.08) !important;
}
.kpi-card, .card, .session-card, .chart-card,
.trade-panel, .panel-block, .modal-box,
.settings-card, .login-card, .backtest-sessions {
  background: rgba(15,18,25,0.85) !important;
  backdrop-filter: blur(8px) !important;
}
.chart-area, .chart-topbar, .balance-bar,
#chart-container, .right-panel, .trade-panel {
  background: rgba(8,10,8,0.95) !important;
}
.quit-bar {
  background: rgba(8,10,8,0.97) !important;
}
</style>"""

html_files = glob.glob('frontend/*.html')
count = 0
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    c = re.sub(r'<style id="bg-global">.*?</style>', '', c, flags=re.DOTALL)
    c = c.replace('</head>', bg_css + '</head>')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    count += 1
    print(filepath + ' done!')

print(str(count) + ' files updated!')