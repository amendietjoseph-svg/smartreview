import re

with open('frontend/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('<link rel="stylesheet" href="/css/dashboard.css">', '')
c = c.replace('<link rel="stylesheet" href="/css/components.css">', '')
c = c.replace('<script src="/js/layout.js"></script>', '')
c = c.replace('<script src="/js/utils.js"></script>', '')
c = c.replace('<script src="/js/dashboard.js"></script>', '')
c = c.replace('<script src="/js/charts.js"></script>', '')
c = c.replace('<div id="app-layout-root"></div>', '')

for tag_id in ['bg-v4','bg-v3','bg-v2','bg-final','bg-global','bg-fix',
               'gradients','kpi-colors','sidebar-bg','global-radius',
               'fs-css','chart-simple-fix','tradecasa-style',
               'buttons-fix','keepalive','accounts-style-fix',
               'coach-spacing','import-style','bg-global','bg-v4']:
    c = re.sub(r'<style id="'+tag_id+'">.*?</style>', '', c, flags=re.DOTALL)
    c = re.sub(r'<script id="'+tag_id+'">.*?</script>', '', c, flags=re.DOTALL)

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')