with open('frontend/backtesting.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix le CSS du trading interface
old_css = '.trading-interface.active { display:grid; grid-template-columns:1fr 320px; height:calc(100vh - 60px); overflow:hidden; }'
new_css = '''.trading-interface.active {
  display: grid;
  grid-template-columns: 1fr 320px;
  height: calc(100vh - 60px);
  overflow: hidden;
  position: relative;
}
.chart-area {
  display: flex !important;
  flex-direction: column !important;
  height: 100% !important;
  overflow: hidden !important;
  background: #131722 !important;
}
#chart-container {
  flex: 1 !important;
  position: relative !important;
  min-height: 0 !important;
  overflow: hidden !important;
}
#chart-inner {
  position: absolute !important;
  left: 36px !important;
  right: 0 !important;
  top: 0 !important;
  bottom: 0 !important;
}
.drawing-tools {
  position: absolute !important;
  left: 0 !important;
  top: 0 !important;
  bottom: 0 !important;
  width: 36px !important;
  z-index: 5 !important;
}'''

c = c.replace(old_css, new_css)

with open('frontend/backtesting.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')