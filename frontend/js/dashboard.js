/**
 * Dashboard functionality for SmartReview - Ultra-Premium Design
 * Handles loading stats, rendering charts, empty states, and backend status
 */

let currentPeriod = '30d';
let equityChart = null;
let buySellChart = null;
let refreshInterval = null;
let isBackendOnline = false;

/**
 * Check backend status
 */
async function checkBackendStatus() {
    const api = new API();
    const statusDot = document.getElementById('backendStatus');
    const statusText = document.getElementById('backendStatusText');
    const backendBanner = document.getElementById('backendBanner');
    
    try {
        const result = await api.healthCheck();
        isBackendOnline = result !== null;
        
        if (isBackendOnline) {
            statusDot.className = 'status-dot online';
            statusText.textContent = 'En ligne';
            backendBanner.classList.add('hidden');
        } else {
            throw new Error('Backend offline');
        }
    } catch (error) {
        isBackendOnline = false;
        statusDot.className = 'status-dot offline';
        statusText.textContent = 'Hors ligne';
        backendBanner.classList.remove('hidden');
        showEmptyStates();
    }
}

/**
 * Load dashboard data
 */
async function loadDashboard() {
    await checkBackendStatus();
    
    if (!isBackendOnline) {
        showEmptyStates();
        return;
    }
    
    try {
        const accountId = getActiveAccountId();
        
        if (!accountId) {
            showEmptyStates();
            return;
        }

        const api = new API();
        
        // Load stats
        const stats = await api.getStats(accountId, currentPeriod);
        updateKPIs(stats);
        
        // Load equity curve
        const equityData = await api.getEquityCurve(accountId, currentPeriod);
        renderEquityChart(equityData.equity_curve);
        
        // Load recent trades
        const trades = await api.getTrades(accountId, 0, 10);
        renderRecentTrades(trades);
        
        // Load accounts for right panel
        const accounts = await api.getAccounts();
        renderAccountsPanel(accounts);
        
        // Render trading score
        renderTradingScore(stats);
        
        // Render buy/sell distribution
        renderBuySellChart(trades);
        
        // Render session performance
        renderSessionPerformance(trades);
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showEmptyStates();
    }
}

/**
 * Update KPI cards
 */
function updateKPIs(stats) {
    if (!stats) {
        showEmptyStates();
        return;
    }
    
    // Row 1 KPIs
    updateKPIValue('totalProfit', stats.net_profit, true);
    updateKPIValue('winRate', stats.win_rate, false, '%');
    updateKPIValue('profitFactor', stats.profit_factor, false);
    updateKPIValue('avgRR', stats.average_rr, false);
    
    // Row 2 KPIs
    updateKPIValue('dailyProfit', stats.daily_profit || 0, true);
    updateKPIValue('monthlyProfit', stats.monthly_profit || 0, true);
    updateKPIValue('currentDrawdown', stats.current_drawdown, false, '%');
    updateKPIValue('maxDrawdown', stats.max_drawdown, false, '%');
}

/**
 * Update single KPI value
 */
function updateKPIValue(elementId, value, isCurrency = false, suffix = '') {
    const element = document.getElementById(elementId);
    const changeElement = document.getElementById(elementId + 'Change');
    
    if (value === null || value === undefined || isNaN(value)) {
        element.textContent = '--';
        element.classList.add('empty');
        if (changeElement) changeElement.textContent = '';
        return;
    }
    
    element.textContent = isCurrency ? formatCurrency(value) : formatNumber(value) + suffix;
    element.classList.remove('empty');
    
    if (changeElement) {
        changeElement.textContent = ''; // No change data from backend yet
    }
}

/**
 * Render equity chart
 */
function renderEquityChart(equityCurve) {
    const chartContainer = document.getElementById('equityChart');
    const equityEmptyState = document.getElementById('equityEmptyState');
    const equityTotal = document.getElementById('equityTotal');
    const equityTrades = document.getElementById('equityTrades');
    
    if (!equityCurve || equityCurve.length === 0) {
        chartContainer.style.display = 'none';
        equityEmptyState.style.display = 'flex';
        equityTotal.textContent = '--';
        equityTrades.textContent = '0';
        return;
    }
    
    chartContainer.style.display = 'block';
    equityEmptyState.style.display = 'none';
    equityTotal.textContent = formatCurrency(equityCurve[equityCurve.length - 1].balance);
    equityTrades.textContent = equityCurve.length;

    const categories = equityCurve.map(point => formatDate(point.date));
    const series = equityCurve.map(point => point.balance);

    if (equityChart) {
        equityChart.destroy();
    }

    const options = {
        series: [{
            name: 'Équité',
            data: series
        }],
        chart: {
            type: 'area',
            height: 280,
            toolbar: { show: false },
            animations: { enabled: true }
        },
        colors: ['#E11D48'],
        fill: {
            type: 'gradient',
            gradient: {
                shadeIntensity: 1,
                opacityFrom: 0.7,
                opacityTo: 0.1,
                stops: [0, 90, 100]
            }
        },
        dataLabels: { enabled: false },
        stroke: {
            curve: 'smooth',
            width: 2
        },
        xaxis: {
            categories: categories,
            labels: {
                style: { colors: '#888888' }
            },
            axisBorder: { show: false },
            axisTicks: { show: false }
        },
        yaxis: {
            labels: {
                style: { colors: '#888888' },
                formatter: (value) => formatCurrency(value)
            }
        },
        grid: {
            borderColor: '#222222',
            strokeDashArray: 4
        },
        tooltip: {
            theme: 'dark',
            y: {
                formatter: (value) => formatCurrency(value)
            }
        }
    };

    equityChart = new ApexCharts(chartContainer, options);
    equityChart.render();
}

/**
 * Render recent trades table
 */
function renderRecentTrades(trades) {
    const tbody = document.getElementById('recentTradesBody');
    
    if (!trades || trades.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6">
                    <div class="empty-state">
                        <i data-lucide="book"></i>
                        <h3>Aucun trade récent</h3>
                        <p>Vos trades apparaîtront ici</p>
                    </div>
                </td>
            </tr>
        `;
        lucide.createIcons();
        return;
    }

    tbody.innerHTML = trades.map(trade => `
        <tr onclick="viewTradeDetails(${trade.id})">
            <td><strong>${trade.asset}</strong></td>
            <td><span class="badge ${trade.direction.toLowerCase()}">${trade.direction}</span></td>
            <td>${formatDate(trade.trade_date)}</td>
            <td class="${trade.profit_loss >= 0 ? 'positive' : 'negative'}">${formatCurrency(trade.profit_loss)}</td>
            <td>${trade.trading_score || '--'}</td>
            <td><span class="badge ${(trade.result || '').toLowerCase()}">${trade.result || 'En cours'}</span></td>
        </tr>
    `).join('');
}

/**
 * Render trading score
 */
function renderTradingScore(stats) {
    const scoreValue = document.getElementById('tradingScoreValue');
    const scoreProgress = document.getElementById('scoreProgress');
    
    const score = stats.average_trading_score || 0;
    
    if (score === 0 || !score) {
        scoreValue.textContent = '--';
        scoreValue.classList.add('empty');
        scoreProgress.style.strokeDasharray = '0, 100';
        
        // Reset sub-metrics
        ['disciplineFill', 'riskFill', 'executionFill', 'coherenceFill'].forEach(id => {
            document.getElementById(id).style.width = '0%';
        });
        return;
    }
    
    scoreValue.textContent = score;
    scoreValue.classList.remove('empty');
    
    const circumference = 2 * Math.PI * 15.9155;
    const offset = circumference - (score / 100) * circumference;
    scoreProgress.style.strokeDasharray = `${circumference - offset}, ${circumference}`;
    
    // Sub-metrics (placeholder values from backend)
    document.getElementById('disciplineFill').style.width = (stats.discipline_score || score) + '%';
    document.getElementById('riskFill').style.width = (stats.risk_score || score) + '%';
    document.getElementById('executionFill').style.width = (stats.execution_score || score) + '%';
    document.getElementById('coherenceFill').style.width = (stats.coherence_score || score) + '%';
}

/**
 * Render buy/sell donut chart
 */
function renderBuySellChart(trades) {
    const chartContainer = document.getElementById('buySellChart');
    const legendContainer = document.getElementById('buySellLegend');
    
    if (!trades || trades.length === 0) {
        chartContainer.innerHTML = `
            <div class="empty-state">
                <i data-lucide="pie-chart"></i>
                <h3>Aucune donnée</h3>
            </div>
        `;
        lucide.createIcons();
        legendContainer.innerHTML = '';
        return;
    }
    
    const buyCount = trades.filter(t => t.direction === 'BUY').length;
    const sellCount = trades.filter(t => t.direction === 'SELL').length;
    const total = trades.length;
    
    if (buySellChart) {
        buySellChart.destroy();
    }
    
    const options = {
        series: [buyCount, sellCount],
        chart: {
            type: 'donut',
            height: 200
        },
        labels: ['BUY', 'SELL'],
        colors: ['#22C55E', '#EF4444'],
        plotOptions: {
            pie: {
                donut: {
                    size: '70%',
                    labels: {
                        show: true,
                        total: {
                            show: true,
                            label: 'Total',
                            formatter: () => total.toString()
                        }
                    }
                }
            }
        },
        dataLabels: { enabled: false },
        legend: { show: false }
    };
    
    buySellChart = new ApexCharts(chartContainer, options);
    buySellChart.render();
    
    legendContainer.innerHTML = `
        <div class="donut-legend-item">
            <div class="donut-legend-color" style="background: #22C55E"></div>
            <span>BUY (${buyCount})</span>
        </div>
        <div class="donut-legend-item">
            <div class="donut-legend-color" style="background: #EF4444"></div>
            <span>SELL (${sellCount})</span>
        </div>
    `;
}

/**
 * Render session performance
 */
function renderSessionPerformance(trades) {
    if (!trades || trades.length === 0) {
        document.getElementById('asiaFill').style.width = '0%';
        document.getElementById('asiaFill').textContent = '--';
        document.getElementById('londonFill').style.width = '0%';
        document.getElementById('londonFill').textContent = '--';
        document.getElementById('nyFill').style.width = '0%';
        document.getElementById('nyFill').textContent = '--';
        return;
    }
    
    const sessions = ['ASIA', 'LONDON', 'NEW_YORK'];
    const fillIds = ['asiaFill', 'londonFill', 'nyFill'];
    
    sessions.forEach((session, index) => {
        const sessionTrades = trades.filter(t => t.session === session);
        const pnl = sessionTrades.reduce((sum, t) => sum + (t.profit_loss || 0), 0);
        const totalPnl = trades.reduce((sum, t) => sum + (t.profit_loss || 0), 0);
        
        const percentage = totalPnl !== 0 ? Math.abs((pnl / totalPnl) * 100) : 0;
        const fillElement = document.getElementById(fillIds[index]);
        
        fillElement.style.width = percentage + '%';
        fillElement.textContent = formatCurrency(pnl);
        
        // Color based on performance
        fillElement.className = 'session-bar-fill';
        if (pnl > 0) {
            fillElement.style.backgroundColor = 'var(--green)';
        } else if (pnl < 0) {
            fillElement.classList.add('red');
        } else {
            fillElement.classList.add('orange');
        }
    });
}

/**
 * Render accounts panel
 */
async function renderAccountsPanel(accounts) {
    const container = document.getElementById('accountsList');
    
    if (!accounts || accounts.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i data-lucide="wallet"></i>
                <h3>Aucun compte</h3>
                <p>Ajoutez votre premier compte pour commencer</p>
            </div>
        `;
        lucide.createIcons();
        return;
    }
    
    container.innerHTML = accounts.map(account => `
        <div class="account-mini-card">
            <div class="account-mini-name">${account.name}</div>
            <div class="account-mini-balance">${formatCurrency(account.current_balance)}</div>
            <div class="account-mini-change ${account.current_balance >= account.initial_balance ? '' : 'negative'}">
                ${formatCurrency(account.current_balance - account.initial_balance)}
            </div>
        </div>
    `).join('');
}

/**
 * Show empty states for all sections
 */
function showEmptyStates() {
    // KPI values
    const kpiElements = [
        'totalProfit', 'winRate', 'profitFactor', 'avgRR',
        'dailyProfit', 'monthlyProfit', 'currentDrawdown', 'maxDrawdown'
    ];
    
    kpiElements.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = '--';
            element.classList.add('empty');
        }
        const changeElement = document.getElementById(id + 'Change');
        if (changeElement) changeElement.textContent = '';
    });
    
    // Equity chart
    document.getElementById('equityChart').innerHTML = `
        <div class="empty-state">
            <i data-lucide="trending-up"></i>
            <h3>Aucun trade enregistré</h3>
            <p>Commencez à trader pour voir votre courbe d'équité</p>
            <button class="btn-primary" onclick="document.getElementById('newTradeBtn').click()">Ajouter un trade</button>
        </div>
    `;
    document.getElementById('equityTotal').textContent = '--';
    document.getElementById('equityPeriod').textContent = '0';
    
    // Recent trades
    document.getElementById('recentTradesBody').innerHTML = `
        <tr>
            <td colspan="6">
                <div class="empty-state">
                    <i data-lucide="book"></i>
                    <h3>Aucun trade récent</h3>
                    <p>Vos trades apparaîtront ici</p>
                </div>
            </td>
        </tr>
    `;
    
    // Trading score
    document.getElementById('tradingScoreValue').textContent = '--';
    document.getElementById('tradingScoreValue').classList.add('empty');
    document.getElementById('scoreProgress').style.strokeDasharray = '0, 100';
    ['disciplineFill', 'riskFill', 'executionFill', 'coherenceFill'].forEach(id => {
        document.getElementById(id).style.width = '0%';
    });
    
    // Buy/Sell chart
    document.getElementById('buySellChart').innerHTML = `
        <div class="empty-state">
            <i data-lucide="pie-chart"></i>
            <h3>Aucune donnée</h3>
        </div>
    `;
    document.getElementById('buySellLegend').innerHTML = '';
    
    // Session performance
    document.getElementById('asiaFill').style.width = '0%';
    document.getElementById('asiaFill').textContent = '--';
    document.getElementById('londonFill').style.width = '0%';
    document.getElementById('londonFill').textContent = '--';
    document.getElementById('nyFill').style.width = '0%';
    document.getElementById('nyFill').textContent = '--';
    
    // Accounts
    document.getElementById('accountsList').innerHTML = `
        <div class="empty-state">
            <i data-lucide="wallet"></i>
            <h3>Aucun compte</h3>
            <p>Ajoutez votre premier compte pour commencer</p>
        </div>
    `;
    
    lucide.createIcons();
}

/**
 * View trade details (placeholder)
 */
function viewTradeDetails(tradeId) {
    // TODO: Implement trade details view
    console.log('View trade:', tradeId);
}

/**
 * Handle account change
 */
function onAccountChange(accountId) {
    loadDashboard();
}

/**
 * Handle period change
 */
function handlePeriodChange(period) {
    currentPeriod = period;
    loadDashboard();
}

/**
 * Update datetime
 */
function updateDateTime() {
    const now = new Date();
    const options = { 
        weekday: 'short', 
        day: 'numeric', 
        month: 'short', 
        hour: '2-digit', 
        minute: '2-digit' 
    };
    document.getElementById('currentDateTime').textContent = now.toLocaleDateString('fr-FR', options);
}

/**
 * Initialize dashboard
 */
function initializeDashboard() {
    // Period selector
    document.querySelectorAll('.period-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.period-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            handlePeriodChange(btn.dataset.period);
        });
    });

    // New trade modal
    const modal = document.getElementById('tradeModal');
    const form = document.getElementById('tradeForm');
    
    document.getElementById('newTradeBtn').addEventListener('click', () => {
        form.reset();
        modal.classList.add('active');
    });
    
    document.getElementById('closeModal').addEventListener('click', () => {
        modal.classList.remove('active');
    });
    
    document.getElementById('cancelModal').addEventListener('click', () => {
        modal.classList.remove('active');
    });

    // Form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = new FormData(form);
        const accountId = getActiveAccountId();
        
        if (!accountId) {
            showToast('Veuillez sélectionner un compte', 'error');
            return;
        }

        const tradeData = {
            account_id: parseInt(accountId),
            asset: formData.get('asset'),
            direction: formData.get('direction'),
            entry_price: parseFloat(formData.get('entry_price')),
            stop_loss: formData.get('stop_loss') ? parseFloat(formData.get('stop_loss')) : null,
            take_profit: formData.get('take_profit') ? parseFloat(formData.get('take_profit')) : null,
            lot_size: parseFloat(formData.get('lot_size')),
            risk_amount: formData.get('risk_amount') ? parseFloat(formData.get('risk_amount')) : null,
            setup: formData.get('setup'),
            session: formData.get('session'),
            confidence_level: formData.get('confidence_level') ? parseInt(formData.get('confidence_level')) : null,
            plan_respected: formData.get('plan_respected') === 'true'
        };

        try {
            const api = new API();
            await api.createTrade(tradeData);
            modal.classList.remove('active');
            showToast('Trade créé avec succès', 'success');
            loadDashboard();
        } catch (error) {
            console.error('Error creating trade:', error);
            showToast('Erreur lors de la création du trade', 'error');
        }
    });

    // Update datetime every minute
    updateDateTime();
    setInterval(updateDateTime, 60000);

    // Initial load
    setTimeout(loadDashboard, 500);

    // Auto-refresh every 30 seconds
    refreshInterval = setInterval(loadDashboard, 30000);
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    initializeCommon();
    initializeDashboard();
});
