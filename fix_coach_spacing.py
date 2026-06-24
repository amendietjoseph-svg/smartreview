with open('frontend/coach.html', 'r', encoding='utf-8') as f:
    c = f.read()

spacing_css = """<style id="coach-spacing">
.hero-actions {
  display: flex !important;
  gap: 12px !important;
  flex-wrap: wrap !important;
  margin-top: 20px !important;
}
.hero-actions button, .coach-action-btn {
  padding: 10px 18px !important;
  border-radius: 12px !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  border: 1px solid rgba(34,197,94,0.3) !important;
  background: rgba(34,197,94,0.1) !important;
  color: #22C55E !important;
  transition: all 0.2s !important;
  white-space: nowrap !important;
}
.hero-actions button:hover, .coach-action-btn:hover {
  background: rgba(34,197,94,0.2) !important;
}
.hero-subtitle {
  margin-bottom: 0 !important;
}
.last-analysis {
  font-size: 12px !important;
  color: #4B5563 !important;
  margin-top: 12px !important;
}
</style>"""

import re
c = re.sub(r'<style id="coach-spacing">.*?</style>', '', c, flags=re.DOTALL)
c = c.replace('</head>', spacing_css + '</head>')

with open('frontend/coach.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')