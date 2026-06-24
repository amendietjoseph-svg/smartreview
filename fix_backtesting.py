with open('frontend/backtesting.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Ajouter widget TradingView après </head>
tv_widget = """
<style id="tv-style">
#tradingview-widget {
  width: 100%;
  height: 500px;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #1E1E1E;
  margin-bottom: 24px;
}
.tv-section {
  margin-bottom: 24px;
}
.tv-section-title {
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 12px;
}
.symbol-selector {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}
.symbol-btn {
  padding: 6px 14px;
  border-radius: 10px;
  border: 1px solid #1E1E1E;
  background: #141414;
  color: #6B7280;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}
.symbol-btn.active, .symbol-btn:hover {
  background: rgba(34,197,94,0.15);
  border-color: rgba(34,197,94,0.3);
  color: #22C55E;
}
</style>"""

# Ajouter le widget TradingView dans le contenu
tv_section = """
<div class="tv-section">
  <div class="tv-section-title">📊 Graphique en Temps Réel</div>
  <div class="symbol-selector">
    <button class="symbol-btn active" onclick="changeSymbol('FX:EURUSD')">EUR/USD</button>
    <button class="symbol-btn" onclick="changeSymbol('FX:GBPUSD')">GBP/USD</button>
    <button class="symbol-btn" onclick="changeSymbol('TVC:GOLD')">XAU/USD</button>
    <button class="symbol-btn" onclick="changeSymbol('CAPITALCOM:US30')">US30</button>
    <button class="symbol-btn" onclick="changeSymbol('NASDAQ:NDX')">NAS100</button>
    <button class="symbol-btn" onclick="changeSymbol('BINANCE:BTCUSDT')">BTC/USD</button>
  </div>
  <div id="tradingview-widget"></div>
</div>

<script>
let tvWidget = null;
let currentSymbol = 'FX:EURUSD';

function loadTradingView(symbol) {
  document.getElementById('tradingview-widget').innerHTML = '';
  new TradingView.widget({
    container_id: 'tradingview-widget',
    symbol: symbol || currentSymbol,
    interval: 'H1',
    timezone: 'Africa/Lagos',
    theme: 'dark',
    style: '1',
    locale: 'fr',
    toolbar_bg: '#0a0a0a',
    enable_publishing: false,
    hide_side_toolbar: false,
    allow_symbol_change: true,
    studies: [],
    width: '100%',
    height: 500,
    backgroundColor: '#0a0a0a',
    gridColor: '#1E1E1E',
  });
}

function changeSymbol(symbol) {
  currentSymbol = symbol;
  document.querySelectorAll('.symbol-btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  loadTradingView(symbol);
}

// Charger TradingView au démarrage
if (typeof TradingView !== 'undefined') {
  loadTradingView();
} else {
  const script = document.createElement('script');
  script.src = 'https://s3.tradingview.com/tv.js';
  script.onload = () => loadTradingView();
  document.head.appendChild(script);
}
</script>"""

import re
c = re.sub(r'<style id="tv-style">.*?</style>', '', c, flags=re.DOTALL)
c = c.replace('</head>', tv_widget + '</head>')

# Insérer le widget avant la section configuration
if 'Configuration du Backtest' in c:
    c = c.replace('<div', tv_section + '\n<div', 1)

with open('frontend/backtesting.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Backtesting done!')