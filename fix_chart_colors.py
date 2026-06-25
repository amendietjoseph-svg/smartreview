with open('frontend/backtesting.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Couleurs bougies style TradersCasa
c = c.replace(
    "upColor:'#22C55E', downColor:'#EF4444'",
    "upColor:'#26a69a', downColor:'#ef5350'"
)
c = c.replace(
    "borderUpColor:'#22C55E', borderDownColor:'#EF4444'",
    "borderUpColor:'#26a69a', borderDownColor:'#ef5350'"
)
c = c.replace(
    "wickUpColor:'#22C55E', wickDownColor:'#EF4444'",
    "wickUpColor:'#26a69a', wickDownColor:'#ef5350'"
)

# 2. Fond graphique style TradersCasa
c = c.replace(
    "background:{type:'solid',color:'#0A0A0A'}",
    "background:{type:'solid',color:'#131722'}"
)
c = c.replace(
    "vertLines:{color:'#1A1A1A'}, horzLines:{color:'#1A1A1A'}",
    "vertLines:{color:'#1e222d'}, horzLines:{color:'#1e222d'}"
)
c = c.replace(
    "textColor:'#9CA3AF'",
    "textColor:'#787b86'"
)

# 3. Ajouter barre outils verticale + lignes SL/TP + settings
extra = """
<style id="tradecasa-style">
/* Barre outils gauche */
.drawing-tools {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 36px;
  background: #1e222d;
  border-right: 1px solid #2a2e39;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 0;
  gap: 2px;
  z-index: 10;
}
.tool-btn {
  width: 28px;
  height: 28px;
  border-radius: 4px;
  background: transparent;
  border: none;
  color: #787b86;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  transition: all 0.15s;
}
.tool-btn:hover, .tool-btn.active {
  background: #2a2e39;
  color: #d1d4dc;
}
.tool-separator {
  width: 20px;
  height: 1px;
  background: #2a2e39;
  margin: 4px 0;
}

/* Chart container avec offset pour tools */
#chart-container {
  position: relative;
}
#chart-inner {
  position: absolute;
  left: 36px;
  right: 0;
  top: 0;
  bottom: 0;
}

/* Bottom bar style TradersCasa */
.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 230px;
  right: 0;
  height: 48px;
  background: #131722;
  border-top: 1px solid #2a2e39;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  z-index: 50;
  font-size: 13px;
  color: #787b86;
}
.bottom-controls-btn {
  background: transparent;
  border: 1px solid #2a2e39;
  color: #787b86;
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.bottom-controls-btn:hover { background: #2a2e39; color: #d1d4dc; }
.bottom-balance { display: flex; align-items: center; gap: 16px; }
.bottom-quit-btn {
  background: rgba(38,166,154,0.15);
  border: 1px solid rgba(38,166,154,0.3);
  color: #26a69a;
  padding: 6px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
}
.bottom-quit-btn:hover { background: rgba(38,166,154,0.25); }

/* Settings panel */
#chartSettingsPanel {
  position: absolute;
  top: 44px;
  right: 0;
  background: #1e222d;
  border: 1px solid #2a2e39;
  border-radius: 8px;
  padding: 16px;
  width: 260px;
  z-index: 100;
  display: none;
  box-shadow: 0 8px 24px rgba(0,0,0,0.5);
}
.settings-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #2a2e39;
  font-size: 12px;
  color: #787b86;
}
.settings-row:last-child { border: none; }
.settings-row input[type=color] {
  width: 36px;
  height: 24px;
  border-radius: 4px;
  border: 1px solid #2a2e39;
  cursor: pointer;
  padding: 0;
}
.settings-row input[type=checkbox] {
  width: 16px;
  height: 16px;
  cursor: pointer;
}
.settings-apply-btn {
  width: 100%;
  margin-top: 12px;
  padding: 8px;
  background: rgba(38,166,154,0.2);
  border: 1px solid rgba(38,166,154,0.4);
  color: #26a69a;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 600;
}

/* Panel droit style TradersCasa */
.trade-panel {
  background: #1e222d !important;
  border-left: 1px solid #2a2e39 !important;
}
.panel-block { border-bottom: 1px solid #2a2e39 !important; }
.panel-block-title { color: #787b86 !important; }
.field-inp {
  background: #131722 !important;
  border: 1px solid #2a2e39 !important;
  color: #d1d4dc !important;
}
.chart-topbar {
  background: #1e222d !important;
  border-bottom: 1px solid #2a2e39 !important;
}
.balance-bar {
  background: #131722 !important;
  border-bottom: 1px solid #2a2e39 !important;
  font-size: 12px !important;
}
.tf-pill {
  background: transparent !important;
  border: none !important;
  color: #787b86 !important;
  border-radius: 4px !important;
}
.tf-pill.active {
  background: #2962ff !important;
  color: #fff !important;
}
.tf-pill:hover:not(.active) { background: #2a2e39 !important; color: #d1d4dc !important; }
.pair-badge {
  background: transparent !important;
  border: none !important;
  color: #d1d4dc !important;
  font-size: 14px !important;
  font-weight: 700 !important;
}
.r-btn { color: #787b86 !important; }
.r-btn:hover, .r-btn.active { color: #26a69a !important; background: #2a2e39 !important; }
</style>

<script id="tradecasa-features">
// Lignes SL/TP sur le graphique
let slLine = null, tpLine = null, entryLine = null;

function updatePriceLines() {
  if(!candleSeries || !allCandles.length) return;
  const currentPrice = allCandles[visibleIndex-1]?.close || 0;
  const sl = parseFloat(document.getElementById('slPips')?.value) || 20;
  const tp = parseFloat(document.getElementById('tpPips')?.value) || 40;
  const pipSize = currentPrice > 100 ? 0.1 : 0.0001;

  // Supprimer les anciennes lignes
  try { if(slLine) candleSeries.removePriceLine(slLine); } catch(e) {}
  try { if(tpLine) candleSeries.removePriceLine(tpLine); } catch(e) {}
  try { if(entryLine) candleSeries.removePriceLine(entryLine); } catch(e) {}

  if(!currentPrice) return;

  slLine = candleSeries.createPriceLine({
    price: currentPrice - sl * pipSize,
    color: '#ef5350',
    lineWidth: 1,
    lineStyle: 2,
    axisLabelVisible: true,
    title: 'SL',
  });
  tpLine = candleSeries.createPriceLine({
    price: currentPrice + tp * pipSize,
    color: '#26a69a',
    lineWidth: 1,
    lineStyle: 2,
    axisLabelVisible: true,
    title: 'TP',
  });
  entryLine = candleSeries.createPriceLine({
    price: currentPrice,
    color: '#ffffff',
    lineWidth: 1,
    lineStyle: 0,
    axisLabelVisible: true,
    title: 'Entry',
  });
}

// Mettre a jour les lignes quand SL/TP changent
document.addEventListener('DOMContentLoaded', function() {
  const slInput = document.getElementById('slPips');
  const tpInput = document.getElementById('tpPips');
  if(slInput) slInput.addEventListener('input', updatePriceLines);
  if(tpInput) tpInput.addEventListener('input', updatePriceLines);

  // Settings panel toggle
  const settingsBtn = document.getElementById('chartSettingsBtn');
  const settingsPanel = document.getElementById('chartSettingsPanel');
  if(settingsBtn && settingsPanel) {
    settingsBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      settingsPanel.style.display = settingsPanel.style.display === 'none' ? 'block' : 'none';
    });
    document.addEventListener('click', function() {
      if(settingsPanel) settingsPanel.style.display = 'none';
    });
  }

  // Apply settings
  const applyBtn = document.getElementById('applyChartSettings');
  if(applyBtn) {
    applyBtn.addEventListener('click', function() {
      if(!chart) return;
      const upColor = document.getElementById('upColorPicker')?.value || '#26a69a';
      const downColor = document.getElementById('downColorPicker')?.value || '#ef5350';
      const bgColor = document.getElementById('bgColorPicker')?.value || '#131722';
      const showGrid = document.getElementById('showGridCheck')?.checked;
      
      candleSeries.applyOptions({
        upColor, downColor,
        borderUpColor: upColor, borderDownColor: downColor,
        wickUpColor: upColor, wickDownColor: downColor,
      });
      chart.applyOptions({
        layout: { background: { color: bgColor } },
        grid: {
          vertLines: { visible: showGrid, color: '#1e222d' },
          horzLines: { visible: showGrid, color: '#1e222d' },
        }
      });
      document.getElementById('chartSettingsPanel').style.display = 'none';
    });
  }
});

// Mettre a jour les lignes apres chaque bougie
const origDisplayCandles = window.displayCandles;
</script>"""

import re
c = re.sub(r'<style id="tradecasa-style">.*?</style>', '', c, flags=re.DOTALL)
c = re.sub(r'<script id="tradecasa-features">.*?</script>', '', c, flags=re.DOTALL)
c = c.replace('</body>', extra + '</body>')

# 4. Remplacer quit-bar par bottom-bar style TradersCasa
c = re.sub(
    r'<div class="quit-bar"[^>]*>.*?</div>\s*</div>',
    '''<div class="bottom-bar" id="quitBar">
      <button class="bottom-controls-btn" onclick="document.querySelector('.trade-panel').classList.toggle('hidden')">
        ☰ Afficher les listes de contrôle
      </button>
      <div class="bottom-balance">
        <span>Équilibre: <strong id="bottomBalance" style="color:#d1d4dc">$10,000.00</strong></span>
        <span>Résultat: <strong id="bottomPnL" style="color:#26a69a">+$0.00</strong></span>
      </div>
      <button class="bottom-quit-btn" onclick="quitSession()">← Quitter la session ↗</button>
    </div>''',
    c, flags=re.DOTALL
)

# 5. Ajouter bouton settings dans chart-topbar
c = c.replace(
    '<button id="fsBtn"',
    '''<div style="position:relative;">
      <button id="chartSettingsBtn" title="Paramètres du graphique"
        style="padding:6px 10px;border-radius:6px;background:#2a2e39;border:1px solid #363a45;color:#787b86;cursor:pointer;font-size:14px;">
        ⚙
      </button>
      <div id="chartSettingsPanel" onclick="event.stopPropagation()">
        <div style="font-size:13px;font-weight:600;color:#d1d4dc;margin-bottom:12px;">Paramètres du graphique</div>
        <div class="settings-row">
          <span>Bougie haussière</span>
          <input type="color" id="upColorPicker" value="#26a69a">
        </div>
        <div class="settings-row">
          <span>Bougie baissière</span>
          <input type="color" id="downColorPicker" value="#ef5350">
        </div>
        <div class="settings-row">
          <span>Fond du graphique</span>
          <input type="color" id="bgColorPicker" value="#131722">
        </div>
        <div class="settings-row">
          <span>Afficher la grille</span>
          <input type="checkbox" id="showGridCheck" checked>
        </div>
        <button class="settings-apply-btn" id="applyChartSettings">✓ Appliquer</button>
      </div>
    </div>
    <button id="fsBtn"''',
    1
)

# 6. Ajouter barre outils gauche dans chart-container
c = c.replace(
    '<div id="chart-container">',
    '''<div id="chart-container" style="position:relative;">
      <div class="drawing-tools">
        <button class="tool-btn active" title="Curseur" onclick="setTool(this)">✛</button>
        <div class="tool-separator"></div>
        <button class="tool-btn" title="Ligne de tendance" onclick="setTool(this)">╱</button>
        <button class="tool-btn" title="Horizontal" onclick="setTool(this)">─</button>
        <button class="tool-btn" title="Rectangle" onclick="setTool(this)">▭</button>
        <button class="tool-btn" title="Flèche" onclick="setTool(this)">↗</button>
        <div class="tool-separator"></div>
        <button class="tool-btn" title="Texte" onclick="setTool(this)">T</button>
        <button class="tool-btn" title="Emoji" onclick="setTool(this)">☺</button>
        <div class="tool-separator"></div>
        <button class="tool-btn" title="Zoom" onclick="setTool(this)">⊕</button>
        <button class="tool-btn" title="Aimant" onclick="setTool(this)">⚇</button>
      </div>
      <div id="chart-inner">'''
)

# Fermer le div chart-inner
c = c.replace(
    '</div>\n\n        <!-- TRADE PANEL -->',
    '</div></div>\n\n        <!-- TRADE PANEL -->'
)

with open('frontend/backtesting.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')