with open('frontend/settings.html', 'r', encoding='utf-8') as f:
    c = f.read()

settings_fix = """<style id="settings-fix">
.settings-section { margin-bottom: 24px; }
.settings-card {
  background: #141414;
  border: 1px solid #1E1E1E;
  border-radius: 16px;
  padding: 24px;
}
.setting-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 0;
  border-bottom: 1px solid #1A1A1A;
}
.setting-row:last-child { border-bottom: none; }
.setting-label { font-size: 14px; color: #fff; font-weight: 500; }
.setting-desc { font-size: 12px; color: #6B7280; margin-top: 2px; }

/* Toggle switch */
.toggle-switch {
  position: relative;
  width: 44px;
  height: 24px;
  appearance: none;
  background: #2A2A2A;
  border-radius: 12px;
  cursor: pointer;
  transition: background 0.2s;
  border: none !important;
  padding: 0 !important;
  flex-shrink: 0;
}
.toggle-switch:checked { background: #22C55E !important; }
.toggle-switch::after {
  content: '';
  position: absolute;
  top: 3px; left: 3px;
  width: 18px; height: 18px;
  background: white;
  border-radius: 50%;
  transition: transform 0.2s;
}
.toggle-switch:checked::after { transform: translateX(20px); }

/* Color dots */
.color-picker-row { display: flex; gap: 10px; }
.color-dot {
  width: 28px; height: 28px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
}
.color-dot.active, .color-dot:hover {
  transform: scale(1.2);
  border-color: white;
}

/* Toggle group */
.toggle-group { display: flex; gap: 4px; }
.toggle-btn {
  padding: 6px 14px;
  border-radius: 8px;
  border: 1px solid #1E1E1E;
  background: #141414;
  color: #6B7280;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.15s;
}
.toggle-btn.active {
  background: rgba(34,197,94,0.15);
  border-color: rgba(34,197,94,0.3);
  color: #22C55E;
}

/* Save button */
.btn-save {
  background: linear-gradient(135deg, #22C55E, #16A34A);
  color: #000;
  border: none;
  padding: 12px 24px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  margin-top: 16px;
  transition: all 0.2s;
}
.btn-save:hover { box-shadow: 0 4px 20px rgba(34,197,94,0.4); transform: translateY(-1px); }

/* Input dans settings */
.settings-card input[type="text"],
.settings-card input[type="email"],
.settings-card input[type="password"],
.settings-card select {
  background: #0F0F0F !important;
  border: 1px solid #1E1E1E !important;
  border-radius: 10px !important;
  color: #fff !important;
  padding: 10px 14px !important;
  width: 200px !important;
}
</style>

<script id="settings-js">
document.addEventListener('DOMContentLoaded', function() {
  // Toggle buttons
  document.querySelectorAll('.toggle-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      this.closest('.toggle-group').querySelectorAll('.toggle-btn')
        .forEach(b => b.classList.remove('active'));
      this.classList.add('active');
    });
  });

  // Color dots
  document.querySelectorAll('.color-dot').forEach(dot => {
    dot.addEventListener('click', function() {
      document.querySelectorAll('.color-dot').forEach(d => d.classList.remove('active'));
      this.classList.add('active');
      const color = this.dataset.color;
      document.documentElement.style.setProperty('--accent', color);
      localStorage.setItem('accentColor', color);
    });
  });

  // Restore accent color
  const savedColor = localStorage.getItem('accentColor');
  if (savedColor) {
    document.documentElement.style.setProperty('--accent', savedColor);
    document.querySelectorAll('.color-dot').forEach(d => {
      if (d.dataset.color === savedColor) d.classList.add('active');
      else d.classList.remove('active');
    });
  }

  // Save button
  const saveBtn = document.querySelector('.btn-save, button[type="submit"]');
  if (saveBtn) {
    saveBtn.addEventListener('click', function(e) {
      e.preventDefault();
      this.textContent = '✓ Sauvegardé !';
      this.style.background = 'linear-gradient(135deg, #22C55E, #16A34A)';
      setTimeout(() => {
        this.textContent = 'Sauvegarder les paramètres';
      }, 2000);
    });
  }

  // Toggle switches
  document.querySelectorAll('.toggle-switch').forEach(toggle => {
    toggle.addEventListener('change', function() {
      localStorage.setItem('toggle_' + this.name, this.checked);
    });
    const saved = localStorage.getItem('toggle_' + toggle.name);
    if (saved !== null) toggle.checked = saved === 'true';
  });
});
</script>"""

import re
c = re.sub(r'<style id="settings-fix">.*?</style>', '', c, flags=re.DOTALL)
c = re.sub(r'<script id="settings-js">.*?</script>', '', c, flags=re.DOTALL)
c = c.replace('</body>', settings_fix + '</body>')

with open('frontend/settings.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Settings done!')