import re

with open('frontend/accounts.html', 'r', encoding='utf-8') as f:
    c = f.read()

fix_js = """<script id="accounts-final-fix">
const ACCT_BASE = window.location.hostname === 'localhost'
  ? 'http://localhost:8001'
  : 'https://smartreview-y4sq.onrender.com';

document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', async function(e) {
      e.preventDefault();
      
      // Collecter les données du formulaire
      const raw = {};
      this.querySelectorAll('input,select,textarea').forEach(el => {
        if(el.name && el.value !== '') {
          raw[el.name] = el.value;
        }
      });
      
      console.log('Raw form data:', raw);
      
      // Construire payload exact selon le schema backend
      const payload = {
        name: raw.name || raw.account_name || 'Mon Compte',
        type: raw.type || raw.account_type || 'PERSONAL',
        broker: raw.broker || 'Autre',
        initial_balance: parseFloat(raw.initial_balance || raw.solde_initial || 10000),
        current_balance: parseFloat(raw.current_balance || raw.solde_actuel || raw.initial_balance || 10000),
        is_active: true
      };
      
      // Champs optionnels
      if(raw.prop_firm_name) payload.prop_firm_name = raw.prop_firm_name;
      if(raw.challenge_phase) payload.challenge_phase = raw.challenge_phase;
      if(raw.profit_target) payload.profit_target = parseFloat(raw.profit_target);
      if(raw.daily_drawdown_limit) payload.daily_drawdown_limit = parseFloat(raw.daily_drawdown_limit);
      if(raw.max_drawdown_limit) payload.max_drawdown_limit = parseFloat(raw.max_drawdown_limit);
      
      console.log('Sending payload:', payload);
      
      try {
        const res = await fetch(ACCT_BASE + '/accounts', {
          method: 'POST',
          headers: {'Content-Type': 'application/json', 'Accept': 'application/json'},
          body: JSON.stringify(payload)
        });
        
        const responseText = await res.text();
        console.log('Response:', res.status, responseText);
        
        if(res.ok) {
          showNotif('✓ Compte créé avec succès!', 'green');
          setTimeout(() => window.location.reload(), 1500);
        } else {
          showNotif('Erreur: ' + responseText, 'red');
        }
      } catch(err) {
        console.error(err);
        showNotif('Erreur réseau: ' + err.message, 'red');
      }
    });
  });
});

function showNotif(msg, color) {
  let n = document.getElementById('acct-notif');
  if(!n) {
    n = document.createElement('div');
    n.id = 'acct-notif';
    n.style.cssText = 'position:fixed;bottom:24px;right:24px;padding:14px 20px;border-radius:12px;font-size:13px;font-weight:600;z-index:9999;color:#fff;';
    document.body.appendChild(n);
  }
  n.textContent = msg;
  n.style.background = color === 'green' ? '#22C55E' : '#EF4444';
  n.style.color = color === 'green' ? '#000' : '#fff';
  n.style.opacity = '1';
  setTimeout(() => n.style.opacity = '0', 4000);
}
</script>"""

c = re.sub(r'<script id="accounts-final-fix">.*?</script>', '', c, flags=re.DOTALL)
c = re.sub(r'<script id="accounts-api-fix">.*?</script>', '', c, flags=re.DOTALL)
c = c.replace('</body>', fix_js + '</body>')

with open('frontend/accounts.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')