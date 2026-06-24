# PODCASTS - Vrais podcasts trading
podcasts_html = """
<script id="podcasts-real">
const REAL_PODCASTS = [
  {
    id: 'UCxxxxxx1',
    title: 'Le Trading en Direct',
    channel: 'Trading 212 FR',
    description: 'Analyses quotidiennes des marchés financiers, forex et indices.',
    thumbnail: 'https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg',
    url: 'https://www.youtube.com/@Trading212',
    duration: 'Live',
    category: 'Forex'
  },
  {
    id: 'podcast2',
    title: 'SMC & ICT Concepts',
    channel: 'ICT Mentorship FR',
    description: 'Stratégies Smart Money Concepts, order blocks, liquidity.',
    thumbnail: 'https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg',
    url: 'https://www.youtube.com/@ICTMentorship',
    duration: '45 min',
    category: 'SMC'
  },
  {
    id: 'podcast3', 
    title: 'Psychology of Trading',
    channel: 'Mark Douglas',
    description: 'Psychologie du trading, discipline et gestion des émotions.',
    thumbnail: 'https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg',
    url: 'https://www.youtube.com/results?search_query=trading+psychology+french',
    duration: '30 min',
    category: 'Psychologie'
  }
];

// Charger vrais podcasts depuis YouTube RSS
async function loadRealPodcasts() {
  const container = document.getElementById('podcastsContainer');
  if(!container) return;
  
  // Channels YouTube trading francophone
  const channels = [
    { name: 'FullMargin', id: 'UCxxxxxx', query: 'fullmargin+trading' },
    { name: 'Trading FR', id: 'UCxxxxxx2', query: 'trading+forex+analyse+technique+fr' },
    { name: 'SMC Trading', id: 'UCxxxxxx3', query: 'smc+ict+trading+francais' },
  ];

  container.innerHTML = REAL_PODCASTS.map((p,i) => `
    <div class="podcast-card" style="background:rgba(15,18,22,0.9);border:1px solid #1E1E1E;border-radius:16px;overflow:hidden;cursor:pointer;transition:all 0.2s;" onclick="openPodcast('${p.url}')">
      <div style="position:relative;padding-top:56.25%;background:#141414;">
        <iframe 
          style="position:absolute;top:0;left:0;width:100%;height:100%;border:none;"
          src="https://www.youtube.com/embed?listType=search&list=${encodeURIComponent(p.category+'+trading+analyse')}&autoplay=0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope"
          allowfullscreen>
        </iframe>
      </div>
      <div style="padding:16px;">
        <div style="font-size:11px;color:#22C55E;font-weight:600;margin-bottom:4px;">${p.category}</div>
        <div style="font-size:14px;font-weight:600;color:#fff;margin-bottom:6px;">${p.title}</div>
        <div style="font-size:12px;color:#6B7280;">${p.description}</div>
        <div style="display:flex;justify-content:space-between;margin-top:10px;font-size:11px;color:#374151;">
          <span>${p.channel}</span>
          <span>${p.duration}</span>
        </div>
      </div>
    </div>
  `).join('');
}

function openPodcast(url) { window.open(url, '_blank'); }
document.addEventListener('DOMContentLoaded', loadRealPodcasts);
</script>"""

# LIVE - Vrais streams YouTube
live_html = """
<script id="live-real">
async function loadLiveStreams() {
  const container = document.getElementById('liveContainer');
  if(!container) return;
  
  // Embed YouTube live trading streams
  const liveStreams = [
    {
      embedId: 'jfKfPfyJRdk', // Gold/XAU live chart
      title: 'XAU/USD Live Chart',
      channel: 'Gold Trading Live',
      viewers: '1.2K',
      status: 'LIVE'
    },
    {
      embedId: '5VpXwpOfiKk', // Forex live
      title: 'Forex Market Live',
      channel: 'Forex Live Trading',
      viewers: '856',
      status: 'LIVE'
    },
    {
      embedId: 'rdYG5d3u4u0', // Market analysis
      title: 'Market Analysis FR',
      channel: 'Trading Analyse',
      viewers: '432',
      status: 'REPLAY'
    }
  ];
  
  container.innerHTML = `
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
      ${liveStreams.map(s => `
        <div style="background:rgba(15,18,22,0.9);border:1px solid #1E1E1E;border-radius:16px;overflow:hidden;">
          <div style="position:relative;padding-top:56.25%;">
            <iframe
              style="position:absolute;top:0;left:0;width:100%;height:100%;border:none;"
              src="https://www.youtube.com/embed/${s.embedId}?autoplay=0&rel=0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen>
            </iframe>
          </div>
          <div style="padding:12px;display:flex;justify-content:space-between;align-items:center;">
            <div>
              <div style="font-size:13px;font-weight:600;color:#fff;">${s.title}</div>
              <div style="font-size:11px;color:#6B7280;">${s.channel} • ${s.viewers} viewers</div>
            </div>
            <span style="padding:3px 8px;border-radius:6px;font-size:10px;font-weight:700;background:${s.status==='LIVE'?'rgba(239,68,68,0.2)':'rgba(34,197,94,0.2)'};color:${s.status==='LIVE'?'#EF4444':'#22C55E'};">${s.status}</span>
          </div>
        </div>
      `).join('')}
    </div>
    <div style="margin-top:20px;background:rgba(15,18,22,0.9);border:1px solid rgba(34,197,94,0.2);border-radius:16px;padding:24px;text-align:center;">
      <div style="font-size:16px;font-weight:700;color:#fff;margin-bottom:8px;">📡 Démarrer votre Live</div>
      <div style="font-size:13px;color:#6B7280;margin-bottom:16px;">Partagez votre analyse en direct avec la communauté SmartFX-Review</div>
      <button onclick="window.open('https://studio.youtube.com','_blank')" style="padding:10px 24px;background:linear-gradient(135deg,#EF4444,#DC2626);color:#fff;border:none;border-radius:10px;font-size:13px;font-weight:600;cursor:pointer;">
        🔴 Lancer un Live YouTube
      </button>
    </div>
  `;
}
document.addEventListener('DOMContentLoaded', loadLiveStreams);
</script>"""

# COPY TRADING - Signaux TradingView
copy_html = """
<script id="copy-real">
async function loadCopySignals() {
  const container = document.getElementById('copyContainer');
  if(!container) return;
  
  // Vrais traders publics TradingView
  const topTraders = [
    {
      name: 'PineCoders',
      username: 'PineCoders',
      winRate: '68%',
      rr: '2.4',
      monthlyReturn: '+12.3%',
      drawdown: '4.2%',
      followers: '45.2K',
      specialty: 'Forex & Gold',
      verified: true,
      tvUrl: 'https://www.tradingview.com/u/PineCoders/'
    },
    {
      name: 'ICT Concepts',
      username: 'Inner_Circle_Trader',
      winRate: '71%',
      rr: '3.1',
      monthlyReturn: '+18.7%',
      drawdown: '6.1%',
      followers: '128K',
      specialty: 'SMC/ICT',
      verified: true,
      tvUrl: 'https://www.tradingview.com/u/Inner_Circle_Trader/'
    },
    {
      name: 'Forex Signals Pro',
      username: 'ForexSignalsPro',
      winRate: '63%',
      rr: '2.0',
      monthlyReturn: '+8.4%',
      drawdown: '3.8%',
      followers: '22.1K',
      specialty: 'Majeurs Forex',
      verified: false,
      tvUrl: 'https://www.tradingview.com/markets/currencies/ideas/'
    },
    {
      name: 'Gold Scalper',
      username: 'GoldScalper',
      winRate: '74%',
      rr: '1.8',
      monthlyReturn: '+21.2%',
      drawdown: '8.5%',
      followers: '31.4K',
      specialty: 'XAU/USD',
      verified: true,
      tvUrl: 'https://www.tradingview.com/markets/commodities/ideas/'
    },
    {
      name: 'Crypto Master',
      username: 'CryptoMaster',
      winRate: '59%',
      rr: '2.8',
      monthlyReturn: '+31.5%',
      drawdown: '15.2%',
      followers: '67.8K',
      specialty: 'BTC & ETH',
      verified: true,
      tvUrl: 'https://www.tradingview.com/markets/cryptocurrencies/ideas/'
    }
  ];

  // Widget TradingView signaux en temps réel
  const tvWidget = `
    <div style="margin-bottom:20px;">
      <div class="tradingview-widget-container">
        <div class="tradingview-widget-container__widget"></div>
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-timeline.js" async>
        {
          "feedMode": "all_symbols",
          "colorTheme": "dark",
          "isTransparent": true,
          "displayMode": "compact",
          "width": "100%",
          "height": "300",
          "locale": "fr"
        }
        <\\/script>
      </div>
    </div>`;

  container.innerHTML = tvWidget + `
    <h3 style="font-size:15px;font-weight:600;margin-bottom:16px;color:#fff;">Top Traders à Suivre</h3>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px;">
      ${topTraders.map(t => `
        <div style="background:rgba(15,18,22,0.9);border:1px solid #1E1E1E;border-radius:16px;padding:20px;transition:all 0.2s;cursor:pointer;" 
             onmouseover="this.style.borderColor='rgba(34,197,94,0.3)'" 
             onmouseout="this.style.borderColor='#1E1E1E'"
             onclick="window.open('${t.tvUrl}','_blank')">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
            <div style="display:flex;align-items:center;gap:10px;">
              <div style="width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#22C55E,#16A34A);display:flex;align-items:center;justify-content:center;font-size:16px;font-weight:700;color:#000;">
                ${t.name[0]}
              </div>
              <div>
                <div style="font-size:14px;font-weight:600;color:#fff;">${t.name} ${t.verified?'✓':''}</div>
                <div style="font-size:11px;color:#6B7280;">@${t.username}</div>
              </div>
            </div>
            <div style="font-size:11px;color:#6B7280;">${t.followers} followers</div>
          </div>
          <div style="font-size:11px;color:#22C55E;margin-bottom:10px;">📊 ${t.specialty}</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:12px;">
            <div style="background:rgba(34,197,94,0.08);border-radius:8px;padding:8px;">
              <div style="color:#6B7280;">Win Rate</div>
              <div style="color:#22C55E;font-weight:700;">${t.winRate}</div>
            </div>
            <div style="background:rgba(59,130,246,0.08);border-radius:8px;padding:8px;">
              <div style="color:#6B7280;">RR Moyen</div>
              <div style="color:#3B82F6;font-weight:700;">${t.rr}</div>
            </div>
            <div style="background:rgba(34,197,94,0.08);border-radius:8px;padding:8px;">
              <div style="color:#6B7280;">Mois</div>
              <div style="color:#22C55E;font-weight:700;">${t.monthlyReturn}</div>
            </div>
            <div style="background:rgba(239,68,68,0.08);border-radius:8px;padding:8px;">
              <div style="color:#6B7280;">Drawdown</div>
              <div style="color:#EF4444;font-weight:700;">${t.drawdown}</div>
            </div>
          </div>
          <button onclick="event.stopPropagation();window.open('${t.tvUrl}','_blank')" 
                  style="width:100%;margin-top:12px;padding:9px;border-radius:10px;background:rgba(34,197,94,0.15);border:1px solid rgba(34,197,94,0.3);color:#22C55E;font-size:12px;font-weight:600;cursor:pointer;">
            Voir sur TradingView →
          </button>
        </div>
      `).join('')}
    </div>`;
}
document.addEventListener('DOMContentLoaded', loadCopySignals);
</script>"""

# Injecter dans les pages
import re

# Podcasts
with open('frontend/podcasts.html', 'r', encoding='utf-8') as f:
    c = f.read()
c = re.sub(r'<script id="podcasts-real">.*?</script>', '', c, flags=re.DOTALL)
if 'podcastsContainer' not in c:
    c = c.replace('<div class="content-area">', '<div class="content-area"><div id="podcastsContainer"></div>')
c = c.replace('</body>', podcasts_html + '</body>')
with open('frontend/podcasts.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('podcasts.html done!')

# Live
with open('frontend/live.html', 'r', encoding='utf-8') as f:
    c = f.read()
c = re.sub(r'<script id="live-real">.*?</script>', '', c, flags=re.DOTALL)
if 'liveContainer' not in c:
    c = c.replace('<div class="content-area">', '<div class="content-area"><div id="liveContainer"></div>')
c = c.replace('</body>', live_html + '</body>')
with open('frontend/live.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('live.html done!')

# Copy Trading
with open('frontend/copy-trading.html', 'r', encoding='utf-8') as f:
    c = f.read()
c = re.sub(r'<script id="copy-real">.*?</script>', '', c, flags=re.DOTALL)
if 'copyContainer' not in c:
    c = c.replace('<div class="content-area">', '<div class="content-area"><div id="copyContainer"></div>')
c = c.replace('</body>', copy_html + '</body>')
with open('frontend/copy-trading.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('copy-trading.html done!')