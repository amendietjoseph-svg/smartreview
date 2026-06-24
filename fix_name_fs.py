import glob, re

# 1. Renommer SmartReview -> SmartFX-Review partout
files = glob.glob('frontend/*.html') + glob.glob('frontend/js/*.js') + glob.glob('frontend/css/*.css')

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    original = c
    c = c.replace('SmartReview', 'SmartFX-Review')
    c = c.replace('Smart Review', 'SmartFX-Review')
    if c != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(c)
        print(filepath + ' renamed!')

# 2. Fix fullscreen backtesting - prendre tout l'ecran
with open('frontend/backtesting.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Remplacer la fonction toggleFullscreen
old_fs = """function toggleFullscreen() {
  const chartArea = document.querySelector('.chart-area');
  const btn = document.getElementById('fsBtn');
  if (!document.fullscreenElement) {
    chartArea.requestFullscreen().then(() => {
      btn.innerHTML = '<i data-lucide="minimize-2" style="width:14px;height:14px;"></i>';
      lucide.createIcons();
    });
  } else {
    document.exitFullscreen().then(() => {
      btn.innerHTML = '<i data-lucide="maximize-2" style="width:14px;height:14px;"></i>';
      lucide.createIcons();
    });
  }
}"""

new_fs = """function toggleFullscreen() {
  const btn = document.getElementById('fsBtn');
  const tradingUI = document.getElementById('tradingInterface');
  
  if (!document.fullscreenElement) {
    // Fullscreen sur tout le trading interface
    tradingUI.requestFullscreen().catch(err => {
      // Fallback: plein ecran via CSS
      tradingUI.style.position = 'fixed';
      tradingUI.style.top = '0';
      tradingUI.style.left = '0';
      tradingUI.style.right = '0';
      tradingUI.style.bottom = '0';
      tradingUI.style.zIndex = '9999';
      tradingUI.style.width = '100vw';
      tradingUI.style.height = '100vh';
      tradingUI.style.gridTemplateColumns = '1fr 320px';
    });
    if(btn) btn.innerHTML = '<i data-lucide="minimize-2" style="width:14px;height:14px;"></i>';
    lucide.createIcons();
  } else {
    document.exitFullscreen();
    tradingUI.style.position = '';
    tradingUI.style.top = '';
    tradingUI.style.left = '';
    tradingUI.style.right = '';
    tradingUI.style.bottom = '';
    tradingUI.style.zIndex = '';
    tradingUI.style.width = '';
    tradingUI.style.height = '';
    if(btn) btn.innerHTML = '<i data-lucide="maximize-2" style="width:14px;height:14px;"></i>';
    lucide.createIcons();
  }
}"""

if old_fs in c:
    c = c.replace(old_fs, new_fs)
    print('Fullscreen function replaced!')
else:
    # Ajouter si pas trouve
    c = c.replace('</body>', '<script>\n' + new_fs + '\n</script>\n</body>')
    print('Fullscreen function added!')

# Ajouter le bouton fullscreen si pas present
if 'fsBtn' not in c:
    fs_btn = """<button onclick="toggleFullscreen()" id="fsBtn" style="padding:6px 10px;border-radius:8px;background:#141414;border:1px solid #1E1E1E;color:#6B7280;cursor:pointer;display:flex;align-items:center;gap:4px;" title="Plein ecran">
      <i data-lucide="maximize-2" style="width:14px;height:14px;"></i>
    </button>"""
    c = c.replace('<button onclick="showAnalytics()"', fs_btn + '\n<button onclick="showAnalytics()"')
    print('Fullscreen button added!')

with open('frontend/backtesting.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Backtesting done!')