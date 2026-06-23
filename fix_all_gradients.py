import glob

# Style gradient à ajouter sur toutes les pages
gradient_css = """
<style id="gradients">
.hero-section, .coach-hero, .page-hero {
  background: linear-gradient(135deg, #052e16 0%, #1e1b4b 100%) !important;
  border-bottom: 1px solid rgba(139,92,246,0.2) !important;
}
.new-trade-btn {
  background: linear-gradient(135deg, #22C55E, #16A34A) !important;
  box-shadow: 0 4px 20px rgba(34,197,94,0.3) !important;
}
.period-btn.active {
  background: linear-gradient(135deg, #22C55E, #16A34A) !important;
  color: #000 !important;
}
.nav-item.active, .sidebar-item.active, .navbar-link.active {
  background: linear-gradient(135deg, rgba(34,197,94,0.15), rgba(139,92,246,0.1)) !important;
}
.kpi-card.green {
  background: linear-gradient(135deg, #141414, #052e16) !important;
  border-color: rgba(34,197,94,0.2) !important;
}
.kpi-card.purple {
  background: linear-gradient(135deg, #141414, #1e1b4b) !important;
  border-color: rgba(139,92,246,0.2) !important;
}
.kpi-card.blue {
  background: linear-gradient(135deg, #141414, #1e3a5f) !important;
  border-color: rgba(59,130,246,0.2) !important;
}
.kpi-card.gold {
  background: linear-gradient(135deg, #141414, #2d1f00) !important;
  border-color: rgba(245,158,11,0.2) !important;
}
.kpi-card.red {
  background: linear-gradient(135deg, #141414, #2d0a0a) !important;
  border-color: rgba(239,68,68,0.2) !important;
}
</style>
</head>"""

html_files = glob.glob('frontend/*.html')
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    # Supprimer ancien style gradients si existe
    if '<style id="gradients">' in c:
        import re
        c = re.sub(r'<style id="gradients">.*?</style>', '', c, flags=re.DOTALL)
    c = c.replace('</head>', gradient_css)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(filepath + ' done!')