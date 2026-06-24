import glob, re

sidebar_css = """<style id="sidebar-bg">
.sidebar {
  background: rgba(3,5,4,0.92) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
}
.navbar {
  background: rgba(3,4,8,0.92) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
}
.new-trade-btn {
  background: linear-gradient(135deg, #22C55E, #16A34A) !important;
}
.sidebar-footer {
  background: transparent !important;
}
.select-input, #activeAccount {
  background: rgba(8,12,10,0.8) !important;
}
.nav-section-label, .sidebar-section-label {
  background: transparent !important;
}
.sidebar-item, .nav-item {
  background: transparent !important;
}
.sidebar-item.active, .nav-item.active {
  background: rgba(34,197,94,0.12) !important;
}
</style>"""

html_files = glob.glob('frontend/*.html')
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    c = re.sub(r'<style id="sidebar-bg">.*?</style>', '', c, flags=re.DOTALL)
    c = c.replace('</head>', sidebar_css + '</head>')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(filepath + ' done!')