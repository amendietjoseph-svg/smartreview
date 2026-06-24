import glob, re

bg_css = """<style id="bg-v2">
html, body {
  min-height: 100vh !important;
  background: radial-gradient(ellipse at 20% 20%, #051a0f 0%, #0a0a1a 40%, #1a0812 100%) !important;
  background-attachment: fixed !important;
}
* {
  background-color: transparent;
}
.sidebar { background: rgba(5,8,6,0.97) !important; }
.navbar { background: rgba(5,8,12,0.97) !important; backdrop-filter: blur(20px) !important; }
.kpi-card { background: rgba(15,18,22,0.9) !important; }
.card, .chart-card, .session-card { background: rgba(15,18,22,0.9) !important; }
.trade-panel, .right-panel { background: rgba(8,10,10,0.97) !important; }
.panel-block { background: transparent !important; }
.chart-topbar, .balance-bar { background: rgba(6,8,8,0.97) !important; }
#chart-container { background: rgba(8,10,8,0.97) !important; }
.chart-area { background: rgba(6,8,8,0.97) !important; }
.quit-bar { background: rgba(6,8,8,0.97) !important; }
.modal-box, .login-card { background: rgba(15,18,22,0.95) !important; backdrop-filter: blur(20px) !important; }
.settings-card { background: rgba(15,18,22,0.9) !important; }
input, select, textarea { background: rgba(10,12,15,0.8) !important; }
table, tr, td, th { background: transparent !important; }
.trades-table tr:hover td { background: rgba(255,255,255,0.03) !important; }
</style>"""

html_files = glob.glob('frontend/*.html')
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    c = re.sub(r'<style id="bg-v2">.*?</style>', '', c, flags=re.DOTALL)
    c = re.sub(r'<style id="bg-global">.*?</style>', '', c, flags=re.DOTALL)
    c = re.sub(r'<style id="bg-fix">.*?</style>', '', c, flags=re.DOTALL)
    c = c.replace('</head>', bg_css + '</head>')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(filepath + ' done!')