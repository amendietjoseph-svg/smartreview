import glob, re

# 1. Fix Coach page - espacer et nettoyer
with open('frontend/coach.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Supprimer double bouton "+"
c = re.sub(r'(\+ Ajouter mon premier trade.*?){2,}', '+ Ajouter mon premier trade', c, flags=re.DOTALL)

# Ajouter padding/espacement hero
c = c.replace('.hero-section {', '''.hero-section {
  padding: 40px 32px !important;
  margin-bottom: 32px !important;''')

with open('frontend/coach.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Coach fixed!')

# 2. Ajouter favicon + logo sur toutes les pages
favicon = '''<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='8' fill='%2322C55E'/><polyline points='6,22 12,14 17,18 22,10 26,10' stroke='white' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round' fill='none'/><circle cx='26' cy='10' r='2.5' fill='white'/></svg>">'''

html_files = glob.glob('frontend/*.html')
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'rel="icon"' not in content:
        content = content.replace('<meta charset="UTF-8">', '<meta charset="UTF-8">\n    ' + favicon)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(filepath + ' favicon added!')

# 3. Fix erreur chargement compte - fallback si backend offline
with open('frontend/js/utils.js', 'r', encoding='utf-8') as f:
    u = f.read()

u = u.replace(
    'Error loading accounts:',
    '// Error loading accounts - suppressed:'
)

# Ajouter fallback pour le sélecteur de compte
fix = '''
async function loadAccountsIntoSelector(selectId) {
  const select = document.getElementById(selectId);
  if(!select) return;
  try {
    const accounts = await API.getAccounts();
    if(accounts && accounts.length > 0) {
      select.innerHTML = accounts.map(a => 
        `<option value="${a.id}">${a.name}</option>`
      ).join('');
    } else {
      select.innerHTML = '<option value="">Aucun compte</option>';
    }
  } catch(e) {
    select.innerHTML = '<option value="">Hors ligne</option>';
  }
}'''

if 'async function loadAccountsIntoSelector' not in u:
    u = u + '\n' + fix

with open('frontend/js/utils.js', 'w', encoding='utf-8') as f:
    f.write(u)
print('Utils fixed!')