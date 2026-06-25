import re

with open('frontend/backtesting.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix le layout grid
c = c.replace(
    '.trading-interface.active { display:grid; grid-template-columns:1fr 320px; height:calc(100vh - 60px); }',
    '.trading-interface.active { display:grid; grid-template-columns:1fr 320px; height:calc(100vh - 60px); overflow:hidden; }'
)

# Fix chart-area
c = c.replace(
    '.chart-area { display:flex; flex-direction:column; background:#0A0A0A; border-right:1px solid #1A1A1A; }',
    '.chart-area { display:flex; flex-direction:column; background:#131722; border-right:1px solid #2a2e39; min-width:0; overflow:hidden; }'
)

# Fix chart-container height
c = c.replace(
    '#chart-container { flex:1; position:relative; min-height:0; }',
    '#chart-container { flex:1; position:relative; min-height:0; overflow:hidden; }'
)

# Fix chart-inner
c = c.replace(
    '<div id="chart-inner">',
    '<div id="chart-inner" style="position:absolute;left:36px;right:0;top:0;bottom:0;">'
)

with open('frontend/backtesting.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')