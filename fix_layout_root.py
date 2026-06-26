import glob, re

for filepath in glob.glob('frontend/*.html'):
    if 'login.html' in filepath or 'backtesting.html' in filepath:
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Ajouter app-layout-root si pas present
    if 'app-layout-root' not in c:
        c = c.replace('<body>', '<body>\n<div id="app-layout-root"></div>')
    
    # S assurer que layout.js est charge
    if 'layout.js' not in c:
        c = c.replace('</body>', '<script src="/js/api.js"></script>\n<script src="/js/layout.js"></script>\n</body>')
    
    # S assurer que lucide est charge
    if 'lucide' not in c:
        c = c.replace('</head>', '<script src="https://unpkg.com/lucide@latest"></script>\n</head>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(filepath + ' done!')