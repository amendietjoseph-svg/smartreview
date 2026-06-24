import re

with open('frontend/accounts.html', 'r', encoding='utf-8') as f:
    c = f.read()

fix = """<style id="accounts-style-fix">
/* Boutons Enregistrer et Annuler */
.form-actions, .modal-actions {
  display: flex !important;
  gap: 12px !important;
  margin-top: 24px !important;
  justify-content: flex-end !important;
}
button[type="submit"], .btn-save, #saveAccountBtn {
  padding: 12px 28px !important;
  background: linear-gradient(135deg, #22C55E, #16A34A) !important;
  color: #000 !important;
  border: none !important;
  border-radius: 12px !important;
  font-size: 14px !important;
  font-weight: 700 !important;
  cursor: pointer !important;
  min-width: 140px !important;
}
button[type="button"].cancel, .btn-cancel, #cancelAccountBtn {
  padding: 12px 28px !important;
  background: #1A1A1A !important;
  color: #6B7280 !important;
  border: 1px solid #2A2A2A !important;
  border-radius: 12px !important;
  font-size: 14px !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  min-width: 120px !important;
}

/* Champs type/devise/broker plus grands */
.form-group select,
.form-group input,
select.form-control,
input.form-control {
  width: 100% !important;
  padding: 12px 14px !important;
  font-size: 14px !important;
  background: #0F0F0F !important;
  border: 1px solid #2A2A2A !important;
  border-radius: 10px !important;
  color: #fff !important;
  font-family: Inter, sans-serif !important;
  min-height: 44px !important;
}

/* Form grid */
.form-grid {
  display: grid !important;
  grid-template-columns: 1fr 1fr !important;
  gap: 16px !important;
}
.form-group {
  display: flex !important;
  flex-direction: column !important;
  gap: 6px !important;
}
.form-group label {
  font-size: 12px !important;
  color: #6B7280 !important;
  font-weight: 500 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.05em !important;
}
.form-group.full-width {
  grid-column: 1 / -1 !important;
}
</style>

<script id="accounts-api-fix">
const ACCT_BASE = window.location.hostname === 'localhost'
  ? 'http://localhost:8001'
  : 'https://smartreview-y4sq.onrender.com';

async function saveAccount(data) {
  // Reveiller Render si endormi
  try {
    await fetch(ACCT_BASE + '/');
  } catch(e) {}
  
  try {
    const method = data.id ? 'PUT' : 'POST';
    const url = data.id ? ACCT_BASE+'/accounts/'+data.id : ACCT_BASE+'/accounts';
    const res = await fetch(url, {
      method,
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(data)
    });
    
    if(res.ok) {
      showToast('Compte sauvegardé !', 'success');
      setTimeout(() => window.location.reload(), 1000);
    } else {
      const err = await res.json().catch(() => ({}));
      showToast('Erreur: ' + (err.detail || 'Vérifiez le backend'), 'error');
    }
  } catch(e) {
    showToast('Backend hors ligne. Réessayez dans 30s.', 'error');
  }
}

function showToast(msg, type) {
  let toast = document.getElementById('acctToast');
  if(!toast) {
    toast = document.createElement('div');
    toast.id = 'acctToast';
    toast.style.cssText = 'position:fixed;bottom:24px;right:24px;padding:14px 20px;border-radius:12px;font-size:13px;font-weight:600;z-index:9999;transition:all 0.3s;';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.style.background = type==='success' ? '#22C55E' : '#EF4444';
  toast.style.color = type==='success' ? '#000' : '#fff';
  toast.style.opacity = '1';
  setTimeout(() => toast.style.opacity = '0', 3000);
}

document.addEventListener('DOMContentLoaded', function() {
  // Intercepter tous les formulaires de compte
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', async function(e) {
      e.preventDefault();
      const data = {};
      this.querySelectorAll('input,select,textarea').forEach(el => {
        if(el.name) {
          if(el.type==='number') data[el.name] = parseFloat(el.value)||0;
          else if(el.type==='checkbox') data[el.name] = el.checked;
          else data[el.name] = el.value;
        }
      });
      if(!data.name) data.name = 'Mon Compte';
      if(!data.type) data.type = 'PERSONAL';
      if(!data.initial_balance) data.initial_balance = 10000;
      if(!data.current_balance) data.current_balance = data.initial_balance;
      if(!data.broker) data.broker = 'Autre';
      await saveAccount(data);
    });
  });

  // Styliser les boutons existants
  document.querySelectorAll('button').forEach(btn => {
    const txt = btn.textContent.trim().toLowerCase();
    if(txt.includes('enregistrer') || txt.includes('sauvegarder') || txt.includes('créer')) {
      btn.style.cssText = 'padding:12px 28px;background:linear-gradient(135deg,#22C55E,#16A34A);color:#000;border:none;border-radius:12px;font-size:14px;font-weight:700;cursor:pointer;min-width:140px;margin-right:8px;';
    }
    if(txt.includes('annuler') || txt.includes('fermer')) {
      btn.style.cssText = 'padding:12px 28px;background:#1A1A1A;color:#6B7280;border:1px solid #2A2A2A;border-radius:12px;font-size:14px;font-weight:600;cursor:pointer;min-width:120px;';
    }
  });
});
</script>"""

c = re.sub(r'<style id="accounts-style-fix">.*?</style>', '', c, flags=re.DOTALL)
c = re.sub(r'<script id="accounts-api-fix">.*?</script>', '', c, flags=re.DOTALL)
c = c.replace('</body>', fix + '</body>')

with open('frontend/accounts.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')