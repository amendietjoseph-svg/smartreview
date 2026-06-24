import glob, re

buttons_js = """
<script id="buttons-fix">
document.addEventListener('DOMContentLoaded', function() {

  // RECHERCHE
  const searchInput = document.getElementById('globalSearch');
  const searchIcon = document.querySelector('.navbar-search-icon');
  if(searchInput) {
    searchInput.addEventListener('keypress', function(e) {
      if(e.key === 'Enter' && this.value.trim()) {
        window.open('https://www.google.com/search?q=' + encodeURIComponent(this.value + ' trading'), '_blank');
      }
    });
  }
  if(searchIcon) {
    searchIcon.style.cursor = 'pointer';
    searchIcon.addEventListener('click', function() {
      if(searchInput) searchInput.focus();
    });
  }

  // NOTIFICATIONS
  const notifBtn = document.getElementById('notifBtn');
  if(notifBtn) {
    notifBtn.addEventListener('click', function() {
      // Créer panel notifications
      let panel = document.getElementById('notifPanel');
      if(panel) { panel.remove(); return; }
      panel = document.createElement('div');
      panel.id = 'notifPanel';
      panel.style.cssText = 'position:fixed;top:64px;right:16px;width:320px;background:#141414;border:1px solid #1E1E1E;border-radius:16px;z-index:1000;box-shadow:0 8px 32px rgba(0,0,0,0.5);';
      panel.innerHTML = `
        <div style="padding:16px;border-bottom:1px solid #1E1E1E;display:flex;justify-content:space-between;align-items:center;">
          <span style="font-size:14px;font-weight:600;">Notifications</span>
          <button onclick="document.getElementById('notifPanel').remove()" style="background:none;border:none;color:#6B7280;cursor:pointer;font-size:18px;">×</button>
        </div>
        <div style="padding:16px;">
          <div style="text-align:center;padding:24px;color:#374151;font-size:13px;">
            <div style="font-size:32px;margin-bottom:8px;">🔔</div>
            Aucune notification pour le moment
          </div>
        </div>`;
      document.body.appendChild(panel);
      document.addEventListener('click', function closePanel(e) {
        if(!panel.contains(e.target) && e.target !== notifBtn) {
          panel.remove();
          document.removeEventListener('click', closePanel);
        }
      }, { once: false });
    });
  }

  // REFRESH
  const refreshBtn = document.getElementById('refreshBtn');
  if(refreshBtn) {
    refreshBtn.addEventListener('click', function() {
      this.style.transform = 'rotate(360deg)';
      this.style.transition = 'transform 0.5s';
      setTimeout(() => { this.style.transform = ''; }, 500);
      window.location.reload();
    });
  }

  // BALANCE PILL
  const balancePill = document.getElementById('balancePill');
  if(balancePill) {
    balancePill.style.cursor = 'pointer';
    balancePill.addEventListener('click', () => window.location.href = 'accounts.html');
  }

  // AVATAR / USER MENU
  const avatarBtn = document.getElementById('userAvatarBtn');
  const dropdown = document.getElementById('userDropdown');
  if(avatarBtn && dropdown) {
    avatarBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
      dropdown.style.cssText = 'display:block;position:absolute;top:100%;right:0;background:#141414;border:1px solid #1E1E1E;border-radius:12px;min-width:180px;z-index:1000;box-shadow:0 8px 24px rgba(0,0,0,0.5);overflow:hidden;';
    });
    document.addEventListener('click', function() {
      if(dropdown) dropdown.style.display = 'none';
    });
  }

  // USER INFO depuis localStorage
  try {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    if(user.name) {
      const initials = document.getElementById('userAvatarInitials');
      const img = document.getElementById('userAvatarImg');
      if(initials) initials.textContent = user.name.slice(0,2).toUpperCase();
      if(img && user.picture) {
        img.src = user.picture;
        img.classList.remove('hidden');
        img.style.display = 'block';
        if(initials) initials.style.display = 'none';
      }
    }
  } catch(e) {}

  // LOGOUT
  const logoutBtn = document.getElementById('logoutBtn');
  if(logoutBtn) {
    logoutBtn.addEventListener('click', function() {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = 'login.html';
    });
  }

  // NOUVEAU TRADE BTN
  const newTradeBtn = document.getElementById('sidebarNewTradeBtn');
  if(newTradeBtn) {
    newTradeBtn.addEventListener('click', function() {
      // Ouvrir modal si sur dashboard
      const modal = document.getElementById('tradeModal');
      if(modal) {
        modal.classList.add('active');
        modal.style.display = 'flex';
      } else {
        window.location.href = 'journal.html';
      }
    });
  }

  // MOBILE MENU
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const sidebar = document.getElementById('sidebar');
  if(mobileMenuBtn && sidebar) {
    mobileMenuBtn.addEventListener('click', function() {
      sidebar.classList.toggle('open');
    });
  }

  // SIDEBAR TOGGLE
  const sidebarToggle = document.getElementById('sidebarToggle');
  const appWrapper = document.getElementById('appWrapper');
  if(sidebarToggle) {
    sidebarToggle.addEventListener('click', function() {
      sidebar && sidebar.classList.toggle('collapsed');
      appWrapper && appWrapper.classList.toggle('sidebar-collapsed');
      localStorage.setItem('sidebarCollapsed', sidebar && sidebar.classList.contains('collapsed'));
    });
    // Restaurer état
    if(localStorage.getItem('sidebarCollapsed') === 'true') {
      sidebar && sidebar.classList.add('collapsed');
      appWrapper && appWrapper.classList.add('sidebar-collapsed');
    }
  }

});
</script>"""

html_files = glob.glob('frontend/*.html')
for filepath in html_files:
    if 'login.html' in filepath:
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    c = re.sub(r'<script id="buttons-fix">.*?</script>', '', c, flags=re.DOTALL)
    c = c.replace('</body>', buttons_js + '</body>')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(filepath + ' done!')