import glob, re

# CSS ultra-simple qui force le gradient partout
bg_css = """<style id="bg-final">
html, body { 
  background: #060810 !important; 
  min-height: 100vh !important;
}
body::before {
  content: '' !important;
  position: fixed !important;
  inset: 0 !important;
  z-index: 0 !important;
  pointer-events: none !important;
  background: 
    radial-gradient(ellipse 80% 60% at 5% 5%, rgba(0,80,40,0.5) 0%, transparent 60%),
    radial-gradient(ellipse 60% 50% at 95% 95%, rgba(80,0,50,0.5) 0%, transparent 60%),
    radial-gradient(ellipse 40% 40% at 50% 50%, rgba(0,20,60,0.4) 0%, transparent 70%) !important;
}
.app-container, .app-wrapper, .main-content,
.content-area, .backtest-sessions,
#sessionsView, #analyticsView,
.page-content, main {
  position: relative !important;
  z-index: 1 !important;
  background: transparent !important;
}
.sidebar {
  position: fixed !important;
  z-index: 100 !important;
  background: rgba(3,5,4,0.97) !important;
}
.navbar {
  position: fixed !important; 
  z-index: 200 !important;
  background: rgba(3,4,8,0.97) !important;
}
</style>"""

html_files = glob.glob('frontend/*.html')
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    for old_id in ['bg-final', 'bg-v3', 'bg-v2', 'bg-global', 'bg-fix']:
        c = re.sub(r'<style id="' + old_id + r'">.*?</style>', '', c, flags=re.DOTALL)
    c = c.replace('</head>', bg_css + '</head>')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(filepath + ' done!')

print('All files updated!')