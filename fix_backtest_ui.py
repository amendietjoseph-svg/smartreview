with open('frontend/backtesting.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Ajouter bouton fullscreen dans chart-topbar
fullscreen_btn = """
<button onclick="toggleFullscreen()" id="fsBtn" style="padding:6px 12px;border-radius:8px;background:#141414;border:1px solid #1E1E1E;color:#6B7280;font-size:12px;cursor:pointer;display:flex;align-items:center;gap:6px;transition:all 0.15s;" title="Plein écran">
  <i data-lucide="maximize-2" style="width:14px;height:14px;"></i>
</button>"""

# Ajouter date/heure dans balance bar
datetime_html = """
<div class="balance-item" style="margin-left:auto;">
  <span class="balance-label">Date & Heure:</span>
  <span class="balance-value" id="liveDateTime" style="color:#8B5CF6;">--</span>
</div>"""

# Ajouter script fullscreen + datetime
extra_js = """
<script>
// Fullscreen
function toggleFullscreen() {
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
}

// Live datetime
function updateDateTime() {
  const now = new Date();
  const days = ['Dim','Lun','Mar','Mer','Jeu','Ven','Sam'];
  const months = ['Jan','Fév','Mar','Avr','Mai','Jun','Jul','Aoû','Sep','Oct','Nov','Déc'];
  const str = days[now.getDay()] + ' ' + now.getDate() + ' ' + months[now.getMonth()] + ' ' + 
    now.getFullYear() + ' ' + 
    String(now.getHours()).padStart(2,'0') + ':' + 
    String(now.getMinutes()).padStart(2,'0') + ':' + 
    String(now.getSeconds()).padStart(2,'0');
  const el = document.getElementById('liveDateTime');
  if(el) el.textContent = str;
}
setInterval(updateDateTime, 1000);
updateDateTime();
</script>"""

# Injecter dans le bon endroit
c = c.replace(
    '<button onclick="showAnalytics()"',
    fullscreen_btn + '\n<button onclick="showAnalytics()"'
)

c = c.replace(
    '<div class="balance-item">\n                        <span class="balance-label">Session:</span>',
    datetime_html + '\n<div class="balance-item">\n                        <span class="balance-label">Session:</span>'
)

c = c.replace('</body>', extra_js + '</body>')

with open('frontend/backtesting.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')