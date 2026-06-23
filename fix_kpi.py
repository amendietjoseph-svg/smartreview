with open('frontend/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

kpi_style = """<style id="kpi-colors">
.kpi-card.green { background: linear-gradient(135deg, #0a1a0f, #052e16) !important; border: 1px solid rgba(34,197,94,0.25) !important; }
.kpi-card.green .kpi-value { color: #22C55E !important; font-size: 30px !important; font-weight: 800 !important; }
.kpi-card.blue { background: linear-gradient(135deg, #0a1020, #1e3a5f) !important; border: 1px solid rgba(59,130,246,0.25) !important; }
.kpi-card.blue .kpi-value { color: #3B82F6 !important; font-size: 30px !important; font-weight: 800 !important; }
.kpi-card.purple { background: linear-gradient(135deg, #0f0a1e, #1e1b4b) !important; border: 1px solid rgba(139,92,246,0.25) !important; }
.kpi-card.purple .kpi-value { color: #8B5CF6 !important; font-size: 30px !important; font-weight: 800 !important; }
.kpi-card.gold { background: linear-gradient(135deg, #1a1200, #2d1f00) !important; border: 1px solid rgba(245,158,11,0.25) !important; }
.kpi-card.gold .kpi-value { color: #F59E0B !important; font-size: 30px !important; font-weight: 800 !important; }
.kpi-card.red { background: linear-gradient(135deg, #1a0a0a, #2d0a0a) !important; border: 1px solid rgba(239,68,68,0.25) !important; }
.kpi-card.red .kpi-value { color: #EF4444 !important; font-size: 30px !important; font-weight: 800 !important; }
.kpi-card.white .kpi-value { color: #FFFFFF !important; font-size: 30px !important; font-weight: 800 !important; }
.kpi-card { border-radius: 20px !important; padding: 22px !important; transition: all 0.2s !important; }
.kpi-card:hover { transform: translateY(-3px) !important; box-shadow: 0 12px 32px rgba(0,0,0,0.5) !important; }
.kpi-title { font-size: 11px !important; font-weight: 600 !important; color: #4B5563 !important; text-transform: uppercase !important; letter-spacing: 0.08em !important; margin-bottom: 10px !important; }
</style>"""

# Supprimer ancien si existe
import re
c = re.sub(r'<style id="kpi-colors">.*?</style>', '', c, flags=re.DOTALL)
c = c.replace('</body>', kpi_style + '</body>')

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')