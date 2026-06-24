import re

# Enlever badge DEMO sur toutes les pages
import glob
for filepath in glob.glob('frontend/*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    c = re.sub(r'<[^>]*>DEMO<[^>]*>', '', c)
    c = re.sub(r'<[^>]*>DÉMO<[^>]*>', '', c)
    c = re.sub(r'badge.*?[Dd][EÉ][Mm][Oo].*?</[^>]+>', '', c, flags=re.DOTALL)
    c = c.replace('DEMO', '').replace('DÉMO', '')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)

print('DEMO badges removed!')

# Fix live avec vrais IDs YouTube
with open('frontend/live.html', 'r', encoding='utf-8') as f:
    c = f.read()

new_live_js = """
<script id="live-real-v2">
function loadLive() {
  const container = document.getElementById('liveContainer');
  if(!container) return;

  // Vrais videos YouTube trading
  const videos = [
    { id: 'xuCn8ux2gbs', title: 'Live Trading XAU/USD', channel: 'ICT Trading', tag: 'REPLAY' },
    { id: 'tQqBtmIVgMw', title: 'Forex Analysis Live', channel: 'Trading FR', tag: 'REPLAY' },
    { id: 'kLFjg9tmKLg', title: 'SMC Concepts Live', channel: 'SMC Trader', tag: 'REPLAY' },
    { id: 'dp8PhLsUcFE', title: 'Gold Market Analysis', channel: 'Gold Trader', tag: 'REPLAY' },
  ];

  container.innerHTML = `
    <div style="padding:24px;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;">
        <h2 style="font-size:20px;font-weight:700;">Live Direct & Replays</h2>
        <button onclick="window.open('https://studio.youtube.com','_blank')" 
          style="padding:9px 18px;background:rgba(239,68,68,0.15);border:1px solid rgba(239,68,68,0.3);color:#EF4444;border-radius:10px;font-size:13px;font-weight:600;cursor:pointer;">
          🔴 Démarrer un Live
        </button>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
        ${videos.map(v => `
          <div style="background:rgba(15,18,22,0.9);border:1px solid #1E1E1E;border-radius:16px;overflow:hidden;">
            <div style="position:relative;padding-top:56.25%;">
              <iframe
                style="position:absolute;top:0;left:0;width:100%;height:100%;border:none;"
                src="https://www.youtube.com/embed/${v.id}?rel=0&modestbranding=1"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen loading="lazy">
              </iframe>
            </div>
            <div style="padding:12px;display:flex;justify-content:space-between;align-items:center;">
              <div>
                <div style="font-size:13px;font-weight:600;color:#fff;">${v.title}</div>
                <div style="font-size:11px;color:#6B7280;">${v.channel}</div>
              </div>
              <span style="padding:3px 8px;border-radius:6px;font-size:10px;font-weight:700;
                background:rgba(34,197,94,0.15);color:#22C55E;">${v.tag}</span>
            </div>
          </div>
        `).join('')}
      </div>
    </div>`;
}
document.addEventListener('DOMContentLoaded', loadLive);
</script>"""

c = re.sub(r'<script id="live-real[^"]*">.*?</script>', '', c, flags=re.DOTALL)
c = re.sub(r'<script id="live-real-v2">.*?</script>', '', c, flags=re.DOTALL)
c = c.replace('</body>', new_live_js + '</body>')

with open('frontend/live.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('live.html done!')