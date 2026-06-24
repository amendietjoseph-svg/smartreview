import re

with open('frontend/accounts.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Remplacer toutes les URLs accounts dans le HTML
c = c.replace("ACCT_BASE + '/accounts'", "ACCT_BASE + '/api/accounts'")
c = c.replace("ACCT_BASE + \"/accounts\"", "ACCT_BASE + \"/api/accounts\"")
c = c.replace("+ '/accounts/'", "+ '/api/accounts/'")
c = c.replace("'/accounts'", "'/api/accounts'")
c = c.replace('"/accounts"', '"/api/accounts"')
c = c.replace(
    "await fetch(ACCT_BASE + '/api/accounts'",
    "await fetch(ACCT_BASE + '/api/accounts'"
)

# Aussi corriger le script accounts-final-fix
c = c.replace(
    "await fetch(ACCT_BASE + '/accounts'",
    "await fetch(ACCT_BASE + '/api/accounts'"
)

with open('frontend/accounts.html', 'w', encoding='utf-8') as f:
    f.write(c)

# Vérifier
with open('frontend/accounts.html', 'r', encoding='utf-8') as f:
    content = f.read()
    
urls = re.findall(r"fetch\([^)]+\)", content)
for u in urls[:10]:
    print(u)
print('Done!')