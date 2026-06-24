with open('frontend/coach.html', 'r', encoding='utf-8') as f:
    c = f.read()

coach_js = """
<script id="coach-api-fix">
const COACH_BASE = window.location.hostname === 'localhost' 
  ? 'http://localhost:8001' 
  : 'https://smartreview-y4sq.onrender.com';

async function analyzePerformances() {
  const btn = document.querySelector('[onclick*="analyz"], #analyzeBtn, .coach-action-btn');
  if(btn) { btn.textContent = '⏳ Analyse en cours...'; btn.disabled = true; }
  
  try {
    const tradesRes = await fetch(COACH_BASE + '/trades');
    const trades = await tradesRes.json();
    
    const res = await fetch(COACH_BASE + '/ai/analyze', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({account_id: null, period: '30d', trades: trades})
    });
    
    const data = await res.json();
    const content = data.content || data.analysis || data.message || JSON.stringify(data);
    
    // Afficher le résultat
    let resultDiv = document.getElementById('analysisResult');
    if(!resultDiv) {
      resultDiv = document.createElement('div');
      resultDiv.id = 'analysisResult';
      resultDiv.style.cssText = 'background:#141414;border:1px solid #1E1E1E;border-radius:16px;padding:24px;margin-top:20px;';
      document.querySelector('.content-area, main, .coach-content').appendChild(resultDiv);
    }
    resultDiv.innerHTML = '<div style="font-size:14px;line-height:1.8;color:#E5E7EB;white-space:pre-wrap;">' + content + '</div>';
    
  } catch(err) {
    alert('Erreur IA Coach: ' + err.message + '. Vérifiez que le backend est en ligne et que la clé ANTHROPIC_API_KEY est configurée sur Render.');
  } finally {
    if(btn) { btn.textContent = '✨ Analyser mes performances'; btn.disabled = false; }
  }
}

// Attacher aux boutons existants
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('[onclick*="analyz"], .coach-action-btn, #analyzeBtn').forEach(btn => {
    btn.addEventListener('click', analyzePerformances);
  });
});
</script>"""

import re
c = re.sub(r'<script id="coach-api-fix">.*?</script>', '', c, flags=re.DOTALL)
c = c.replace('</body>', coach_js + '</body>')

with open('frontend/coach.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')