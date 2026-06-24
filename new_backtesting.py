content = open('frontend/backtesting.html', 'r', encoding='utf-8').read()

# Nouveau contenu backtesting inspiré TradersCasa
new_content = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartReview - Backtesting</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <script src="https://s3.tradingview.com/tv.js"></script>
    <link rel="stylesheet" href="/css/global.css">
    <style>
        .backtest-layout {
            display: grid;
            grid-template-columns: 1fr 340px;
            gap: 0;
            height: calc(100vh - 60px);
            overflow: hidden;
        }
        .chart-panel {
            display: flex;
            flex-direction: column;
            background: #0A0A0A;
            border-right: 1px solid #1A1A1A;
        }
        .chart-toolbar {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 16px;
            background: #0F0F0F;
            border-bottom: 1px solid #1A1A1A;
            flex-shrink: 0;
        }
        .symbol-select {
            background: #141414;
            border: 1px solid #1E1E1E;
            border-radius: 10px;
            color: #fff;
            padding: 8px 12px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            min-width: 140px;
        }
        .tf-btn {
            padding: 6px 12px;
            border-radius: 8px;
            border: 1px solid #1E1E1E;
            background: #141414;
            color: #6B7280;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s;
        }
        .tf-btn.active, .tf-btn:hover {
            background: rgba(34,197,94,0.15);
            border-color: rgba(34,197,94,0.3);
            color: #22C55E;
        }
        #tv-chart {
            flex: 1;
            width: 100%;
        }
        .right-panel {
            display: flex;
            flex-direction: column;
            background: #0A0A0A;
            overflow-y: auto;
        }
        .panel-section {
            padding: 16px;
            border-bottom: 1px solid #1A1A1A;
        }
        .panel-title {
            font-size: 12px;
            font-weight: 600;
            color: #4B5563;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 12px;
        }
        .trade-btns {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin-bottom: 16px;
        }
        .btn-buy {
            padding: 14px;
            border-radius: 12px;
            border: none;
            background: linear-gradient(135deg, #22C55E, #16A34A);
            color: #000;
            font-size: 14px;
            font-weight: 800;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 4px 16px rgba(34,197,94,0.3);
        }
        .btn-buy:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(34,197,94,0.4); }
        .btn-sell {
            padding: 14px;
            border-radius: 12px;
            border: none;
            background: linear-gradient(135deg, #EF4444, #DC2626);
            color: #fff;
            font-size: 14px;
            font-weight: 800;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 4px 16px rgba(239,68,68,0.3);
        }
        .btn-sell:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(239,68,68,0.4); }
        .input-group {
            margin-bottom: 12px;
        }
        .input-label {
            font-size: 11px;
            color: #6B7280;
            margin-bottom: 6px;
            font-weight: 500;
        }
        .trade-input {
            width: 100%;
            background: #141414;
            border: 1px solid #1E1E1E;
            border-radius: 10px;
            color: #fff;
            padding: 10px 12px;
            font-size: 13px;
            font-family: Inter, sans-serif;
        }
        .trade-input:focus {
            border-color: rgba(34,197,94,0.3);
            outline: none;
        }
        .stat-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #0F0F0F;
        }
        .stat-row:last-child { border-bottom: none; }
        .stat-label { font-size: 12px; color: #6B7280; }
        .stat-value { font-size: 13px; font-weight: 600; color: #fff; }
        .stat-value.positive { color: #22C55E; }
        .stat-value.negative { color: #EF4444; }
        .trades-list { max-height: 300px; overflow-y: auto; }
        .trade-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 12px;
            background: #141414;
            border-radius: 10px;
            margin-bottom: 6px;
            border: 1px solid #1E1E1E;
        }
        .trade-direction {
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 6px;
        }
        .trade-direction.buy { background: rgba(34,197,94,0.15); color: #22C55E; }
        .trade-direction.sell { background: rgba(239,68,68,0.15); color: #EF4444; }
        .rr-display {
            background: #141414;
            border: 1px solid #1E1E1E;
            border-radius: 10px;
            padding: 12px;
            text-align: center;
            margin-bottom: 12px;
        }
        .rr-value {
            font-size: 28px;
            font-weight: 800;
            color: #22C55E;
        }
        .rr-label { font-size: 11px; color: #6B7280; }
        .progress-bar {
            height: 6px;
            background: #1E1E1E;
            border-radius: 3px;
            overflow: hidden;
            margin-top: 4px;
        }
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #22C55E, #16A34A);
            border-radius: 3px;
            transition: width 0.3s;
        }
        .session-badge {
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: 600;
            background: rgba(34,197,94,0.1);
            color: #22C55E;
            border: 1px solid rgba(34,197,94,0.2);
        }
        .empty-trades {
            text-align: center;
            padding: 24px;
            color: #374151;
            font-size: 13px;
        }
    </style>
</head>
<body style="margin:0;background:#0A0A0A;color:#fff;font-family:Inter,sans-serif;">
    <div id="app-layout-root"></div>
    <div class="app-wrapper" id="appWrapper">
        <div class="backtest-layout">
            <!-- CHART PANEL -->
            <div class="chart-panel">
                <div class="chart-toolbar">
                    <select class="symbol-select" id="symbolSelect" onchange="changeSymbol(this.value)">
                        <option value="FX:EURUSD">EUR/USD</option>
                        <option value="FX:GBPUSD">GBP/USD</option>
                        <option value="TVC:GOLD">XAU/USD (Gold)</option>
                        <option value="CAPITALCOM:US30">US30 (Dow)</option>
                        <option value="NASDAQ:NDX">NAS100</option>
                        <option value="FX:USDJPY">USD/JPY</option>
                        <option value="BINANCE:BTCUSDT">BTC/USDT</option>
                        <option value="BINANCE:ETHUSDT">ETH/USDT</option>
                    </select>
                    <div style="display:flex;gap:4px;">
                        <button class="tf-btn" onclick="changeTF(this,\'1\')">M1</button>
                        <button class="tf-btn" onclick="changeTF(this,\'5\')">M5</button>
                        <button class="tf-btn" onclick="changeTF(this,\'15\')">M15</button>
                        <button class="tf-btn active" onclick="changeTF(this,\'60\')">H1</button>
                        <button class="tf-btn" onclick="changeTF(this,\'240\')">H4</button>
                        <button class="tf-btn" onclick="changeTF(this,\'D\')">D1</button>
                    </div>
                    <div style="margin-left:auto;display:flex;align-items:center;gap:8px;">
                        <span style="font-size:12px;color:#6B7280;" id="currentPrice">--</span>
                        <div class="session-badge" id="sessionBadge">LONDON</div>
                    </div>
                </div>
                <div id="tv-chart"></div>
            </div>

            <!-- RIGHT PANEL -->
            <div class="right-panel">
                <!-- TRADE ENTRY -->
                <div class="panel-section">
                    <div class="panel-title">Entrer un Trade</div>
                    <div class="trade-btns">
                        <button class="btn-buy" onclick="enterTrade(\'BUY\')">▲ BUY</button>
                        <button class="btn-sell" onclick="enterTrade(\'SELL\')">▼ SELL</button>
                    </div>
                    <div class="input-group">
                        <div class="input-label">Stop Loss (pips)</div>
                        <input type="number" class="trade-input" id="slInput" placeholder="20" value="20">
                    </div>
                    <div class="input-group">
                        <div class="input-label">Take Profit (pips)</div>
                        <input type="number" class="trade-input" id="tpInput" placeholder="40" value="40">
                    </div>
                    <div class="input-group">
                        <div class="input-label">Risque ($)</div>
                        <input type="number" class="trade-input" id="riskInput" placeholder="100" value="100">
                    </div>
                    <div class="rr-display">
                        <div class="rr-value" id="rrDisplay">2.0</div>
                        <div class="rr-label">Risk/Reward Ratio</div>
                    </div>
                </div>

                <!-- STATS -->
                <div class="panel-section">
                    <div class="panel-title">Statistiques</div>
                    <div class="stat-row">
                        <span class="stat-label">Trades Total</span>
                        <span class="stat-value" id="statTotal">0</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Win Rate</span>
                        <span class="stat-value positive" id="statWR">0%</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">P&L Total</span>
                        <span class="stat-value" id="statPL">$0</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Profit Factor</span>
                        <span class="stat-value" id="statPF">0</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">RR Moyen</span>
                        <span class="stat-value" id="statRR">0</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Meilleure série</span>
                        <span class="stat-value positive" id="statBest">0</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-label">Pire série</span>
                        <span class="stat-value negative" id="statWorst">0</span>
                    </div>
                    <div style="margin-top:12px;">
                        <div style="display:flex;justify-content:space-between;font-size:11px;color:#6B7280;margin-bottom:4px;">
                            <span>Progression</span>
                            <span id="progressPct">0%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" id="progressFill" style="width:0%"></div>
                        </div>
                    </div>
                </div>

                <!-- TRADES LIST -->
                <div class="panel-section">
                    <div class="panel-title">Historique des Trades</div>
                    <div class="trades-list" id="tradesList">
                        <div class="empty-trades">Aucun trade — Cliquez BUY ou SELL</div>
                    </div>
                </div>

                <!-- RESET -->
                <div class="panel-section">
                    <button onclick="resetBacktest()" style="width:100%;padding:12px;border-radius:12px;border:1px solid #1E1E1E;background:#141414;color:#EF4444;font-size:13px;font-weight:600;cursor:pointer;">
                        🗑 Réinitialiser le Backtest
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script src="/js/api.js"></script>
    <script src="/js/layout.js"></script>
    <script>
        // TradingView Widget
        let tvWidget = null;
        let currentSymbol = \'FX:EURUSD\';
        let currentTF = \'60\';
        let trades = JSON.parse(localStorage.getItem(\'backtest_trades\') || \'[]\');

        function initTV() {
            if (tvWidget) tvWidget.remove();
            tvWidget = new TradingView.widget({
                container_id: \'tv-chart\',
                symbol: currentSymbol,
                interval: currentTF,
                timezone: \'Africa/Lagos\',
                theme: \'dark\',
                style: \'1\',
                locale: \'fr\',
                toolbar_bg: \'#0F0F0F\',
                enable_publishing: false,
                hide_side_toolbar: false,
                allow_symbol_change: true,
                studies: [\'RSI@tv-basicstudies\', \'MASimple@tv-basicstudies\'],
                width: \'100%\',
                height: window.innerHeight - 120,
                backgroundColor: \'#0A0A0A\',
            });
        }

        function changeSymbol(symbol) {
            currentSymbol = symbol;
            initTV();
        }

        function changeTF(btn, tf) {
            currentTF = tf;
            document.querySelectorAll(\'.tf-btn\').forEach(b => b.classList.remove(\'active\'));
            btn.classList.add(\'active\');
            initTV();
        }

        // RR Calculator
        document.getElementById(\'slInput\').addEventListener(\'input\', updateRR);
        document.getElementById(\'tpInput\').addEventListener(\'input\', updateRR);

        function updateRR() {
            const sl = parseFloat(document.getElementById(\'slInput\').value) || 1;
            const tp = parseFloat(document.getElementById(\'tpInput\').value) || 1;
            const rr = (tp / sl).toFixed(2);
            document.getElementById(\'rrDisplay\').textContent = rr;
            document.getElementById(\'rrDisplay\').style.color = rr >= 2 ? \'#22C55E\' : rr >= 1 ? \'#F59E0B\' : \'#EF4444\';
        }

        function enterTrade(direction) {
            const sl = parseFloat(document.getElementById(\'slInput\').value) || 20;
            const tp = parseFloat(document.getElementById(\'tpInput\').value) || 40;
            const risk = parseFloat(document.getElementById(\'riskInput\').value) || 100;
            const rr = tp / sl;
            
            // Simuler WIN/LOSS basé sur probabilité
            const winRate = 0.55;
            const isWin = Math.random() < winRate;
            const pnl = isWin ? risk * rr : -risk;
            
            const trade = {
                id: Date.now(),
                direction,
                sl, tp, risk, rr: rr.toFixed(2),
                result: isWin ? \'WIN\' : \'LOSS\',
                pnl: pnl.toFixed(2),
                symbol: currentSymbol.split(\':\')[1],
                time: new Date().toLocaleTimeString(\'fr\')
            };
            
            trades.push(trade);
            localStorage.setItem(\'backtest_trades\', JSON.stringify(trades));
            updateStats();
            renderTrades();
        }

        function updateStats() {
            const total = trades.length;
            const wins = trades.filter(t => t.result === \'WIN\').length;
            const wr = total > 0 ? ((wins/total)*100).toFixed(1) : 0;
            const totalPL = trades.reduce((s,t) => s + parseFloat(t.pnl), 0);
            const grossProfit = trades.filter(t=>t.result===\'WIN\').reduce((s,t)=>s+parseFloat(t.pnl),0);
            const grossLoss = Math.abs(trades.filter(t=>t.result===\'LOSS\').reduce((s,t)=>s+parseFloat(t.pnl),0));
            const pf = grossLoss > 0 ? (grossProfit/grossLoss).toFixed(2) : grossProfit > 0 ? \'∞\' : \'0\';
            const avgRR = total > 0 ? (trades.reduce((s,t)=>s+parseFloat(t.rr),0)/total).toFixed(2) : 0;
            
            // Séries
            let bestStreak = 0, worstStreak = 0, cur = 0;
            trades.forEach(t => {
                if(t.result===\'WIN\') { cur = cur >= 0 ? cur+1 : 1; bestStreak = Math.max(bestStreak,cur); }
                else { cur = cur <= 0 ? cur-1 : -1; worstStreak = Math.min(worstStreak,cur); }
            });

            document.getElementById(\'statTotal\').textContent = total;
            document.getElementById(\'statWR\').textContent = wr + \'%\';
            document.getElementById(\'statWR\').className = \'stat-value \' + (wr >= 50 ? \'positive\' : \'negative\');
            document.getElementById(\'statPL\').textContent = (totalPL >= 0 ? \'+\' : \'\') + \'$\' + totalPL.toFixed(2);
            document.getElementById(\'statPL\').className = \'stat-value \' + (totalPL >= 0 ? \'positive\' : \'negative\');
            document.getElementById(\'statPF\').textContent = pf;
            document.getElementById(\'statRR\').textContent = avgRR;
            document.getElementById(\'statBest\').textContent = bestStreak + \' wins\';
            document.getElementById(\'statWorst\').textContent = Math.abs(worstStreak) + \' losses\';
            
            const progress = Math.min(100, (wins/Math.max(total,1))*100);
            document.getElementById(\'progressFill\').style.width = progress + \'%\';
            document.getElementById(\'progressPct\').textContent = wr + \'%\';
        }

        function renderTrades() {
            const list = document.getElementById(\'tradesList\');
            if(trades.length === 0) {
                list.innerHTML = \'<div class="empty-trades">Aucun trade — Cliquez BUY ou SELL</div>\';
                return;
            }
            list.innerHTML = [...trades].reverse().map(t => `
                <div class="trade-item">
                    <div>
                        <span class="trade-direction ${t.direction.toLowerCase()}">${t.direction}</span>
                        <span style="font-size:11px;color:#6B7280;margin-left:6px;">${t.symbol}</span>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:13px;font-weight:700;color:${parseFloat(t.pnl)>=0?\'#22C55E\':\'#EF4444\'}">${parseFloat(t.pnl)>=0?\'+\':\'\'}\$${t.pnl}</div>
                        <div style="font-size:10px;color:#374151;">RR ${t.rr} • ${t.time}</div>
                    </div>
                </div>
            `).join(\'\');
        }

        function resetBacktest() {
            if(confirm(\'Réinitialiser tous les trades du backtest ?\')) {
                trades = [];
                localStorage.removeItem(\'backtest_trades\');
                updateStats();
                renderTrades();
            }
        }

        // Déterminer session
        function getSession() {
            const h = new Date().getUTCHours();
            if(h >= 7 && h < 9) return {name:\'FRANKFURT\', color:\'#F59E0B\'};
            if(h >= 7 && h < 16) return {name:\'LONDON\', color:\'#3B82F6\'};
            if(h >= 12 && h < 21) return {name:\'NEW YORK\', color:\'#22C55E\'};
            return {name:\'ASIA\', color:\'#8B5CF6\'};
        }
        const session = getSession();
        const badge = document.getElementById(\'sessionBadge\');
        badge.textContent = session.name;
        badge.style.background = session.color + \'20\';
        badge.style.color = session.color;
        badge.style.borderColor = session.color + \'40\';

        // Init
        window.addEventListener(\'load\', () => {
            initTV();
            updateStats();
            renderTrades();
        });
        lucide.createIcons();
    </script>
</body>
</html>'''

open('frontend/backtesting.html', 'w', encoding='utf-8').write(new_content)
print('Backtesting rewritten!')