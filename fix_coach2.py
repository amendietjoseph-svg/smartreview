with open('frontend/coach.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Corriger le gradient cassé
c = c.replace(
    'background: linear-gradient(135deg, #0F2027, #1A1A2E, #16213E)(135deg, var(--accent) 0%, #8B5CF6 100%)',
    'background: linear-gradient(135deg, #052e16 0%, #1e1b4b 100%)'
)

# Corriger le titre avec gradient texte
c = c.replace(
    '.hero-title {\n            font-size: 32px;\n            font-weight: 700;\n            margin-bottom: var(--spacing-sm);\n        }',
    '.hero-title { font-size: 32px; font-weight: 800; margin-bottom: 8px; background: linear-gradient(90deg, #22C55E, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }'
)

with open('frontend/coach.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')