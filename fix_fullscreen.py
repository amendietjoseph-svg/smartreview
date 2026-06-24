with open('frontend/backtesting.html', 'r', encoding='utf-8') as f:
    c = f.read()

fs_css = """<style id="fs-css">
:-webkit-full-screen .sidebar,
:-webkit-full-screen .navbar,
:-webkit-full-screen #quitBar,
:fullscreen .sidebar,
:fullscreen .navbar,
:fullscreen #quitBar {
  display: none !important;
}
:-webkit-full-screen #tradingInterface,
:fullscreen #tradingInterface {
  position: fixed !important;
  top: 0 !important; left: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  z-index: 99999 !important;
  grid-template-columns: 1fr 320px !important;
}
:-webkit-full-screen .chart-area,
:fullscreen .chart-area {
  height: 100vh !important;
}
:-webkit-full-screen #main-chart iframe,
:fullscreen #main-chart iframe {
  height: calc(100vh - 120px) !important;
}
</style>"""

import re
c = re.sub(r'<style id="fs-css">.*?</style>', '', c, flags=re.DOTALL)
c = c.replace('</head>', fs_css + '</head>')

new_fs = """function toggleFullscreen() {
  const btn = document.getElementById('fsBtn');
  const el = document.getElementById('tradingInterface');
  if (!document.fullscreenElement) {
    el.requestFullscreen();
    if(btn) btn.innerHTML = '<i data-lucide="minimize-2" style="width:14px;height:14px;"></i>';
  } else {
    document.exitFullscreen();
    if(btn) btn.innerHTML = '<i data-lucide="maximize-2" style="width:14px;height:14px;"></i>';
  }
  setTimeout(() => lucide.createIcons(), 100);
}"""

c = re.sub(r'function toggleFullscreen\(\)\s*\{.*?\}', new_fs, c, flags=re.DOTALL)

with open('frontend/backtesting.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')