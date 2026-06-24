with open('frontend/backtesting.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Ajouter bouton fullscreen dans chart-topbar
fs_btn = """<button id="fsBtn" onclick="toggleFullscreen()" style="padding:6px 10px;border-radius:8px;background:#141414;border:1px solid #1E1E1E;color:#6B7280;cursor:pointer;display:flex;align-items:center;gap:4px;margin-left:8px;" title="Plein ecran">
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/></svg>
</button>"""

fs_js = """
<script id="fs-script">
function toggleFullscreen() {
  const el = document.getElementById('tradingInterface');
  const btn = document.getElementById('fsBtn');
  if (!document.fullscreenElement) {
    if(el.requestFullscreen) el.requestFullscreen();
    else if(el.webkitRequestFullscreen) el.webkitRequestFullscreen();
    btn.style.color = '#22C55E';
  } else {
    if(document.exitFullscreen) document.exitFullscreen();
    else if(document.webkitExitFullscreen) document.webkitExitFullscreen();
    btn.style.color = '#6B7280';
  }
}
document.addEventListener('fullscreenchange', function() {
  const sidebar = document.querySelector('.sidebar');
  const navbar = document.querySelector('.navbar');
  const quitBar = document.getElementById('quitBar');
  if(document.fullscreenElement) {
    if(sidebar) sidebar.style.display = 'none';
    if(navbar) navbar.style.display = 'none';
    if(quitBar) quitBar.style.left = '0';
  } else {
    if(sidebar) sidebar.style.display = '';
    if(navbar) navbar.style.display = '';
    if(quitBar) quitBar.style.left = '';
  }
});
</script>"""

import re
# Supprimer ancien script fs
c = re.sub(r'<script id="fs-script">.*?</script>', '', c, flags=re.DOTALL)

# Ajouter bouton avant "Analytique"
c = c.replace('<button onclick="showAnalytics()"', fs_btn + '\n<button onclick="showAnalytics()"')

# Ajouter script avant </body>
c = c.replace('</body>', fs_js + '\n</body>')

with open('frontend/backtesting.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')