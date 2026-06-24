with open('frontend/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

new_style = """<style id="login-redesign">
body {
  background: radial-gradient(ellipse at top left, #052e16 0%, #0a0a0a 40%, #1a0a2e 100%) !important;
  min-height: 100vh !important;
}
body::before {
  content: '';
  position: fixed;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: 
    radial-gradient(circle at 20% 20%, rgba(34,197,94,0.15) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(168,85,247,0.15) 0%, transparent 50%),
    radial-gradient(circle at 50% 50%, rgba(34,197,94,0.05) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}
.login-container {
  position: relative;
  z-index: 1;
  max-width: 520px !important;
  width: 100% !important;
  padding: 40px 20px !important;
}
.login-card {
  background: rgba(20,20,20,0.85) !important;
  backdrop-filter: blur(20px) !important;
  border: 1px solid rgba(34,197,94,0.15) !important;
  border-radius: 24px !important;
  padding: 40px !important;
  box-shadow: 
    0 0 80px rgba(34,197,94,0.08),
    0 0 40px rgba(168,85,247,0.08),
    0 32px 64px rgba(0,0,0,0.5) !important;
}
.login-title {
  font-size: 32px !important;
  font-weight: 800 !important;
  background: linear-gradient(135deg, #22C55E, #A855F7) !important;
  -webkit-background-clip: text !important;
  -webkit-text-fill-color: transparent !important;
  background-clip: text !important;
}
.login-subtitle {
  color: #6B7280 !important;
  font-size: 15px !important;
}
.google-btn {
  border-radius: 14px !important;
  padding: 16px !important;
  font-size: 15px !important;
  font-weight: 600 !important;
  border: 1px solid rgba(255,255,255,0.1) !important;
  box-shadow: 0 4px 16px rgba(0,0,0,0.3) !important;
}
.form-input {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(255,255,255,0.08) !important;
  border-radius: 14px !important;
  padding: 16px !important;
  font-size: 15px !important;
  color: #fff !important;
}
.form-input:focus {
  border-color: rgba(34,197,94,0.4) !important;
  box-shadow: 0 0 0 3px rgba(34,197,94,0.1) !important;
}
.login-btn {
  background: linear-gradient(135deg, #22C55E, #16A34A) !important;
  border-radius: 14px !important;
  padding: 16px !important;
  font-size: 15px !important;
  font-weight: 700 !important;
  box-shadow: 0 4px 20px rgba(34,197,94,0.3) !important;
  -webkit-text-fill-color: white !important;
}
.login-btn:hover {
  box-shadow: 0 8px 32px rgba(34,197,94,0.4) !important;
  transform: translateY(-2px) !important;
}
.divider { color: #374151 !important; }
.form-label { color: #9CA3AF !important; font-size: 13px !important; }
.logo svg rect { fill: url(#logoGrad) !important; }
</style>"""

import re
c = re.sub(r'<style id="login-redesign">.*?</style>', '', c, flags=re.DOTALL)
c = c.replace('</body>', new_style + '</body>')

with open('frontend/login.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')