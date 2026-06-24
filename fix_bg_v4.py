import glob, re

bg_css = """<style id="bg-v4">
html {
  height: 100%;
  background: 
    radial-gradient(ellipse 70% 50% at 0% 0%, rgba(0,80,40,0.6) 0%, transparent 55%),
    radial-gradient(ellipse 60% 50% at 100% 100%, rgba(80,0,50,0.6) 0%, transparent 55%),
    radial-gradient(ellipse 50% 60% at 100% 0%, rgba(0,20,80,0.4) 0%, transparent 55%),
    #060810 !important;
  background-attachment: fixed !important;
  background-repeat: no-repeat !important;
  background-size: cover !important;
}
body {
  background: transparent !important;
  min-height: 100vh !important;
}
.app-wrapper, .main-content, .content-area,
#sessionsView, #analyticsView,
.backtest-sessions, .app-container {
  background: transparent !important;
}
.sidebar { background: rgba(3,5,4,0.97) !important; }
.navbar { background: rgba(3,4,8,0.97) !important; }
</style>"""

html_files = glob.glob('frontend/*.html')
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    for old_id in ['bg-v4','bg-final','bg-v3','bg-v2','bg-global','bg-fix']:
        c = re.sub(r'<style id="'+old_id+'">.*?</style>', '', c, flags=re.DOTALL)
    c = c.replace('</head>', bg_css + '</head>')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(filepath + ' done!')