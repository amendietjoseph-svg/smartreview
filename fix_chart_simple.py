import re

with open('frontend/backtesting.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Supprimer drawing-tools et chart-inner qui cassent le layout
c = re.sub(r'<div class="drawing-tools">.*?</div>', '', c, flags=re.DOTALL)
c = c.replace('<div id="chart-inner" style="position:absolute;left:36px;right:0;top:0;bottom:0;">', '')
c = c.replace('<div id="chart-inner">', '')
# Fermer le div chart-inner manquant
c = c.replace('</div></div>\n\n        <!-- TRADE PANEL -->', '\n\n        <!-- TRADE PANEL -->')

# Fix CSS simple
simple_css = """<style id="chart-simple-fix">
.trading-interface.active {
  display: grid !important;
  grid-template-columns: 1fr 320px !important;
  height: calc(100vh - 60px) !important;
  overflow: hidden !important;
}
.chart-area {
  display: flex !important;
  flex-direction: column !important;
  min-width: 0 !important;
  overflow: hidden !important;
  background: #131722 !important;
}
#chart-container {
  flex: 1 !important;
  min-height: 0 !important;
  overflow: hidden !important;
}
.trade-panel {
  overflow-y: auto !important;
  height: 100% !important;
  background: #1e222d !important;
}
</style>"""

c = re.sub(r'<style id="chart-simple-fix">.*?</style>', '', c, flags=re.DOTALL)
c = c.replace('</head>', simple_css + '</head>')

with open('frontend/backtesting.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')