import glob, re

keepalive = """<script id="keepalive">
const API_BASE = window.location.hostname === 'localhost'
  ? 'http://localhost:8001'
  : 'https://smartreview-y4sq.onrender.com';

// Reveiller le backend au chargement
async function wakeBackend() {
  try {
    const res = await fetch(API_BASE + '/', {method:'GET'});
    const statusDot = document.getElementById('backendStatus');
    const statusText = document.getElementById('backendStatusText');
    if(res.ok) {
      if(statusDot) statusDot.className = 'status-dot online';
      if(statusText) statusText.textContent = 'En ligne';
    }
  } catch(e) {
    const statusDot = document.getElementById('backendStatus');
    const statusText = document.getElementById('backendStatusText');
    if(statusDot) statusDot.className = 'status-dot offline';
    if(statusText) statusText.textContent = 'Hors ligne';
  }
}

// Ping toutes les 10 minutes pour garder le backend actif
wakeBackend();
setInterval(wakeBackend, 10 * 60 * 1000);
</script>"""

html_files = glob.glob('frontend/*.html')
for filepath in html_files:
    if 'login.html' in filepath:
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    c = re.sub(r'<script id="keepalive">.*?</script>', '', c, flags=re.DOTALL)
    c = c.replace('</body>', keepalive + '</body>')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(filepath + ' done!')