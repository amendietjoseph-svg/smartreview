import glob, re

bg_css = """<style id="bg-fix">
html, body {
  min-height: 100vh !important;
  width: 100% !important;
  background: linear-gradient(135deg, #050d0a 0%, #0a0a1a 50%, #120a0f 100%) !important;
  background-attachment: fixed !important;
}
.app-wrapper, .main-content, .content-area {
  background: transparent !important;
}
.sidebar {
  background: rgba(8,8,12,0.95) !important;
}
.navbar {
  background: rgba(6,10,8,0.95) !important;
  backdrop-filter: blur(20px) !important;
}
.kpi-card, .card, .chart-card, .session-card,
.trade-panel, .panel-block, .modal-box,
.settings-card, .login-card {
  background: rgba(20,20,28,0.8) !important;
  backdrop-filter: blur(10px) !important;
}
</style>"""

html_files = glob.glob('frontend/*.html')
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    c = re.sub(r'<style id="bg-fix">.*?</style>', '', c, flags=re.DOTALL)
    c = c.replace('</head>', bg_css + '</head>')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(filepath + ' done!')