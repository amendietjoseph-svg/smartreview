with open('frontend/coach.html', 'r', encoding='utf-8') as f:
    c = f.read()

old = 'IA Coach SmartReview'
new = 'IA Coach SmartReview'

# Ajouter gradient hero
gradient_style = """<style>
.coach-hero {
  background: linear-gradient(135deg, #052e16 0%, #1e1b4b 50%, #0a0a0a 100%) !important;
  border-bottom: 1px solid rgba(139,92,246,0.3);
  padding: 32px !important;
  margin-bottom: 24px;
}
.coach-hero h1 {
  font-size: 32px !important;
  font-weight: 800 !important;
  background: linear-gradient(90deg, #22C55E, #8B5CF6);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.coach-action-btn {
  background: rgba(34,197,94,0.15) !important;
  border: 1px solid rgba(34,197,94,0.3) !important;
  color: #22C55E !important;
  padding: 10px 18px !important;
  border-radius: 12px !important;
  font-weight: 600 !important;
  cursor: pointer;
  transition: all 0.2s;
}
.coach-action-btn:hover {
  background: rgba(34,197,94,0.25) !important;
}
</style>"""

c = c.replace('</head>', gradient_style + '</head>')

with open('frontend/coach.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')