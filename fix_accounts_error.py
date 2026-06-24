with open('frontend/accounts.html', 'r', encoding='utf-8') as f:
    c = f.read()

fix_js = """
<script id="accounts-fix">
document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('accountForm') || document.querySelector('form');
  if(!form) return;
  
  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(form);
    const data = {};
    
    // Collecter tous les champs
    form.querySelectorAll('input, select, textarea').forEach(el => {
      if(el.name) {
        if(el.type === 'checkbox') data[el.name] = el.checked;
        else if(el.type === 'number') data[el.name] = parseFloat(el.value) || 0;
        else data[el.name] = el.value;
      }
    });
    
    // Valeurs par defaut obligatoires
    if(!data.name) data.name = 'Mon Compte';
    if(!data.type) data.type = 'PERSONAL';
    if(!data.initial_balance) data.initial_balance = 10000;
    if(!data.current_balance) data.current_balance = data.initial_balance;
    if(!data.broker) data.broker = 'Autre';
    
    try {
      const BASE = window.location.hostname === 'localhost' 
        ? 'http://localhost:8001' 
        : 'https://smartreview-y4sq.onrender.com';
      
      const method = data.id ? 'PUT' : 'POST';
      const url = data.id ? BASE + '/accounts/' + data.id : BASE + '/accounts';
      
      const res = await fetch(url, {
        method: method,
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
      });
      
      if(res.ok) {
        alert('Compte sauvegardé avec succès !');
        window.location.reload();
      } else {
        const err = await res.json();
        console.error('Server error:', err);
        alert('Erreur: ' + (err.detail || JSON.stringify(err)));
      }
    } catch(err) {
      console.error('Network error:', err);
      alert('Erreur réseau: Le backend est peut-être hors ligne. Vérifiez la connexion.');
    }
  });
});
</script>"""

import re
c = re.sub(r'<script id="accounts-fix">.*?</script>', '', c, flags=re.DOTALL)
c = c.replace('</body>', fix_js + '</body>')

with open('frontend/accounts.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')