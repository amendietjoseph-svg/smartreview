import glob, re

# 1. Fix background global - gradient vert/bleu/rose
with open('frontend/css/global.css', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    'background: #0A0A0A;',
    'background: linear-gradient(135deg, #050d0a 0%, #0a0a1a 50%, #120a0f 100%);'
)
c = c.replace(
    '--bg-primary: #0A0A0A;',
    '--bg-primary: #060d0a;'
)

with open('frontend/css/global.css', 'w', encoding='utf-8') as f:
    f.write(c)
print('Background fixed!')

# 2. Fix double bouton Nouveau Trade dans layout.js
with open('frontend/js/layout.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Supprimer le bouton Nouveau Trade du layout si deja dans sidebar
c = re.sub(r'Nouveau Trade.*?Nouveau Trade', 'Nouveau Trade', c, flags=re.DOTALL)

with open('frontend/js/layout.js', 'w', encoding='utf-8') as f:
    f.write(c)
print('Layout fixed!')

# 3. Fix "Erreur de chargement" -> "Aucun compte"
with open('frontend/js/utils.js', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    "'Chargement...'",
    "'Aucun compte'"
)
c = c.replace(
    '"Chargement..."',
    '"Aucun compte"'
)
c = c.replace(
    'Erreur de chargement',
    'Aucun compte'
)

with open('frontend/js/utils.js', 'w', encoding='utf-8') as f:
    f.write(c)
print('Utils fixed!')