/**
 * Advanced Statistics for SmartFX-Review
 * Handles all charts, filtering, and data visualization
 */

let allTrades = [];
let filteredTrades = [];
let charts = {};
let comparisonMode = false;

/**
 * Initialize stats page
 */
async function initializeStats() {
    await loadTrades();
    setupEventListeners();
    populateFilters();
    applyFilters();
}

/**
 * Load trades from backend
 */
async function loadTrades() {
    try {
        const accountId = getActiveAccountId();
        
        if (!accountId) {
            return;
        }

        allTrades = await API.getTrades(accountId);
        filteredTrades = [...allTrades];
        
    } catch (error) {
        console.error('Error loading trades:', error);
    }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Filter changes
    document.getElementById('periodFilter').addEventListener('change', applyFilters);
    document.getElementById('accountFilter').addEventListener('change', applyFilters);
    document.getElementById('assetFilter').addEventListener('change', applyFilters);
    document.getElementById('setupFilter').addEventListener('change', applyFilters);
    document.getElementById('sessionFilter').addEventListener('change', applyFilters);
    
    // Reset filters
    document.getElementById('resetFiltersBtn').addEventListener('click', resetFilters);
    
    // Export stats
    document.getElementById('exportStatsBtn').addEventListener('click', exportStats);
    
    // Comparison mode
    document.getElementById('comparisonModeBtn').addEventListener('click', toggleComparisonMode);
    
    // Comparison period changes
    document.getElementById('comparisonPeriod1').addEventListener('change', updateComparisonCharts);
    document.getElementById('comparisonPeriod2').addEventListener('change', updateComparisonCharts);
    
    // Account change
    const accountSelector = document.getElementById('activeAccount');
    if (accountSelector) {
        accountSelector.addEventListener('change', () => {
            loadTrades().then(() => {
                populateFilters();
                applyFilters();
            });
        });
    }

    // Logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }
}

/**
 * Populate filter dropdowns
 */
function populateFilters() {
    // Assets
    const assets = [...new Set(allTrades.map(t => t.asset).filter(Boolean))];
    const assetFilter = document.getElementById('assetFilter');
    assetFilter.innerHTML = '<option value="">Tous</option>' + 
        assets.map(a => `<option value="${a}">${a}</option>`).join('');
    
    // Setups
    const setups = [...new Set(allTrades.map(t => t.setup).filter(Boolean))];
    const setupFilter = document.getElementById('setupFilter');
    setupFilter.innerHTML = '<option value="">Tous</option>' + 
        setups.map(s => `<option value="${s}">${s}</option>`).join('');
}

/**
 * Apply filters
 */
function applyFilters() {
    const period = document.getElementById('periodFilter').value;
    const account = document.getElementById('accountFilter').value;
    const asset = document.getElementById('assetFilter').value;
    const setup = document.getElementById('setupFilter').value;
    const session = document.getElementById('sessionFilter').value;
    
    filteredTrades = allTrades.filter(trade => {
        // Period filter
        if (period !== 'all') {
            const tradeDate = new Date(trade.trade_date);
            const now = new Date();
            const periodMap = {
                '7d': 7,
                '30d': 30,
                '90d': 90,
                '180d': 180,
                '1y': 365
            };
            const days = periodMap[period] || 30;
            const cutoff = new Date(now - days * 24 * 60 * 60 * 1000);
            if (tradeDate < cutoff) return false;
        }
        
        // Account filter
        if (account && trade.account_id !== parseInt(account)) return false;
        
        // Asset filter
        if (asset && trade.asset !== asset) return false;
        
        // Setup filter
        if (setup && trade.setup !== setup) return false;
        
        // Session filter
        if (session && trade.session !== session) return false;
        
        return true;
    });
    
    renderAllCharts();
    renderHeatmap();
    renderStatsTable();
}

/**
 * Reset filters
 */
function resetFilters() {
    document.getElementById('periodFilter').value = '30d';
    document.getElementById('accountFilter').value = '';
    document.getElementById('assetFilter').value = '';
    document.getElementById('setupFilter').value = '';
    document.getElementById('sessionFilter').value = '';
    applyFilters();
}

/**
 * Render all charts with sequential animation
 */
function renderAllCharts() {
    const chartConfigs = [
        { id: 'equityCurveChart', fn: renderEquityCurveChart },
        { id: 'pnlDayChart', fn: renderPnLDayChart },
        { id: 'buySellChart', fn: renderBuySellChart },
        { id: 'setupPerformanceChart', fn: renderSetupPerformanceChart },
        { id: 'sessionPerformanceChart', fn: renderSessionPerformanceChart },
        { id: 'assetPerformanceChart', fn: renderAssetPerformanceChart },
        { id: 'tradingScoreChart', fn: renderTradingScoreChart },
        { id: 'rrDistributionChart', fn: renderRRDistributionChart },
        { id: 'confidenceCorrelationChart', fn: renderConfidenceCorrelationChart }
    ];
    
    chartConfigs.forEach((config, index) => {
        setTimeout(() => {
            config.fn();
        }, index * 100);
    });
}

/**
 * Render Equity Curve Chart
 */
function renderEquityCurveChart() {
    if (charts.equityCurveChart) charts.equityCurveChart.destroy();
    
    // Calculate equity curve
    const sortedTrades = [...filteredTrades].sort((a, b) => new Date(a.trade_date) - new Date(b.trade_date));
    let cumulative = 0;
    const equityData = sortedTrades.map(trade => {
        cumulative += trade.profit_loss || 0;
        return {
            x: new Date(trade.trade_date).getTime(),
            y: cumulative
        };
    });
    
    // Find best and worst days
    const dailyPnL = {};
    sortedTrades.forEach(trade => {
        const date = trade.trade_date.split('T')[0];
        if (!dailyPnL[date]) dailyPnL[date] = 0;
        dailyPnL[date] += trade.profit_loss || 0;
    });
    
    const bestDay = Object.entries(dailyPnL).sort((a, b) => b[1] - a[1])[0];
    const worstDay = Object.entries(dailyPnL).sort((a, b) => a[1] - b[1])[0];
    
    const annotations = {};
    if (bestDay) {
        annotations[`best-${bestDay[0]}`] = {
            x: new Date(bestDay[0]).getTime(),
            y: equityData.find(e => new Date(e.x).toDateString() === new Date(bestDay[0]).toDateString())?.y,
            borderColor: '#00D26A',
            label: { style: { color: '#00D26A' }, text: `Meilleur: ${formatCurrency(bestDay[1])}` }
        };
    }
    if (worstDay) {
        annotations[`worst-${worstDay[0]}`] = {
            x: new Date(worstDay[0]).getTime(),
            y: equityData.find(e => new Date(e.x).toDateString() === new Date(worstDay[0]).toDateString())?.y,
            borderColor: '#FF4757',
            label: { style: { color: '#FF4757' }, text: `Pire: ${formatCurrency(worstDay[1])}` }
        };
    }
    
    const options = {
        series: [{
            name: 'Équité',
            data: equityData
        }],
        chart: {
            type: 'area',
            height: 350,
            fontFamily: 'Inter, sans-serif',
            background: 'transparent',
            toolbar: { show: true },
            zoom: { enabled: true }
        },
        colors: ['#3B82F6'],
        fill: {
            type: 'gradient',
            gradient: {
                shadeIntensity: 1,
                opacityFrom: 0.7,
                opacityTo: 0.1,
                stops: [0, 90, 100]
            }
        },
        annotations: { points: annotations },
        xaxis: {
            type: 'datetime',
            labels: { style: { colors: '#8B9AB1', fontSize: '12px' } }
        },
        yaxis: {
            labels: {
                style: { colors: '#8B9AB1', fontSize: '12px' },
                formatter: (value) => formatCurrency(value)
            }
        },
        grid: { borderColor: '#1E2330', strokeDashArray: 4 },
        tooltip: {
            theme: 'dark',
            x: { format: 'dd MMM yyyy' },
            y: { formatter: (value) => formatCurrency(value) }
        }
    };
    
    charts.equityCurveChart = new ApexCharts(document.getElementById('equityCurveChart'), options);
    charts.equityCurveChart.render();
}

/**
 * Render P&L by Day Chart
 */
function renderPnLDayChart() {
    if (charts.pnlDayChart) charts.pnlDayChart.destroy();
    
    const dailyPnL = {};
    filteredTrades.forEach(trade => {
        const date = trade.trade_date.split('T')[0];
        if (!dailyPnL[date]) dailyPnL[date] = { pnl: 0, trades: 0 };
        dailyPnL[date].pnl += trade.profit_loss || 0;
        dailyPnL[date].trades += 1;
    });
    
    const sortedDays = Object.keys(dailyPnL).sort();
    const avgPnL = sortedDays.reduce((sum, day) => sum + dailyPnL[day].pnl, 0) / sortedDays.length;
    
    const options = {
        series: [{
            name: 'P&L',
            data: sortedDays.map(day => dailyPnL[day].pnl)
        }],
        chart: {
            type: 'bar',
            height: 350,
            fontFamily: 'Inter, sans-serif',
            background: 'transparent',
            toolbar: { show: false }
        },
        colors: sortedDays.map(day => dailyPnL[day].pnl >= 0 ? '#00D26A' : '#FF4757'),
        plotOptions: {
            bar: { borderRadius: 4, columnWidth: '60%' }
        },
        xaxis: {
            categories: sortedDays.map(d => new Date(d).toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit' })),
            labels: { style: { colors: '#8B9AB1', fontSize: '12px' } }
        },
        yaxis: {
            labels: {
                style: { colors: '#8B9AB1', fontSize: '12px' },
                formatter: (value) => formatCurrency(value)
            }
        },
        grid: { borderColor: '#1E2330', strokeDashArray: 4 },
        tooltip: {
            theme: 'dark',
            y: { formatter: (value) => formatCurrency(value) },
            custom: ({ series, seriesIndex, dataPointIndex, w }) => {
                const day = sortedDays[dataPointIndex];
                return `<div>${day}<br>P&L: ${formatCurrency(series[0][dataPointIndex])}<br>Trades: ${dailyPnL[day].trades}</div>`;
            }
        }
    };
    
    charts.pnlDayChart = new ApexCharts(document.getElementById('pnlDayChart'), options);
    charts.pnlDayChart.render();
}

/**
 * Render Buy/Sell Distribution Chart
 */
function renderBuySellChart() {
    if (charts.buySellChart) charts.buySellChart.destroy();
    
    const buyTrades = filteredTrades.filter(t => t.direction === 'BUY');
    const sellTrades = filteredTrades.filter(t => t.direction === 'SELL');
    
    const buyWins = buyTrades.filter(t => t.result === 'WIN').length;
    const sellWins = sellTrades.filter(t => t.result === 'WIN').length;
    
    const buyWR = buyTrades.length > 0 ? (buyWins / buyTrades.length * 100).toFixed(1) : 0;
    const sellWR = sellTrades.length > 0 ? (sellWins / sellTrades.length * 100).toFixed(1) : 0;
    
    const options = {
        series: [buyTrades.length, sellTrades.length],
        labels: [`BUY (${buyWR}%)`, `SELL (${sellWR}%)`],
        chart: {
            type: 'donut',
            height: 350,
            fontFamily: 'Inter, sans-serif',
            background: 'transparent'
        },
        colors: ['#3B82F6', '#8B5CF6'],
        plotOptions: {
            pie: {
                donut: {
                    size: '70%',
                    labels: {
                        show: true,
                        total: {
                            show: true,
                            label: 'Total',
                            formatter: () => filteredTrades.length.toString()
                        }
                    }
                }
            }
        },
        dataLabels: { enabled: false },
        legend: {
            position: 'bottom',
            labels: { colors: '#8B9AB1' }
        }
    };
    
    charts.buySellChart = new ApexCharts(document.getElementById('buySellChart'), options);
    charts.buySellChart.render();
}

/**
 * Render Performance by Setup Chart
 */
function renderSetupPerformanceChart() {
    if (charts.setupPerformanceChart) charts.setupPerformanceChart.destroy();
    
    const setupStats = {};
    filteredTrades.forEach(trade => {
        if (!trade.setup) return;
        if (!setupStats[trade.setup]) {
            setupStats[trade.setup] = { pnl: 0, trades: 0, wins: 0 };
        }
        setupStats[trade.setup].pnl += trade.profit_loss || 0;
        setupStats[trade.setup].trades += 1;
        if (trade.result === 'WIN') setupStats[trade.setup].wins += 1;
    });
    
    const sortedSetups = Object.entries(setupStats)
        .sort((a, b) => b[1].pnl - a[1].pnl);
    
    const options = {
        series: [{
            data: sortedSetups.map(([_, stats]) => stats.pnl)
        }],
        chart: {
            type: 'bar',
            height: 350,
            fontFamily: 'Inter, sans-serif',
            background: 'transparent',
            toolbar: { show: false }
        },
        plotOptions: {
            bar: {
                borderRadius: 4,
                horizontal: true,
                barHeight: '60%'
            }
        },
        colors: sortedSetups.map(([_, stats]) => {
            const wr = (stats.wins / stats.trades * 100);
            if (wr >= 60) return '#00D26A';
            if (wr >= 40) return '#F59E0B';
            return '#FF4757';
        }),
        xaxis: {
            categories: sortedSetups.map(([setup, _]) => setup),
            labels: { style: { colors: '#8B9AB1', fontSize: '12px' } }
        },
        yaxis: {
            labels: {
                style: { colors: '#8B9AB1', fontSize: '12px' },
                formatter: (value) => formatCurrency(value)
            }
        },
        grid: { borderColor: '#1E2330', strokeDashArray: 4 },
        tooltip: {
            theme: 'dark',
            y: { formatter: (value) => formatCurrency(value) },
            custom: ({ series, seriesIndex, dataPointIndex, w }) => {
                const [setup, stats] = sortedSetups[dataPointIndex];
                const wr = (stats.wins / stats.trades * 100).toFixed(1);
                return `<div>${setup}<br>WR: ${wr}%<br>P&L: ${formatCurrency(stats.pnl)}<br>Trades: ${stats.trades}</div>`;
            }
        }
    };
    
    charts.setupPerformanceChart = new ApexCharts(document.getElementById('setupPerformanceChart'), options);
    charts.setupPerformanceChart.render();
}

/**
 * Render Performance by Session Chart
 */
function renderSessionPerformanceChart() {
    if (charts.sessionPerformanceChart) charts.sessionPerformanceChart.destroy();
    
    const sessionStats = {
        'ASIA': { pnl: 0, trades: 0, wins: 0, rr: 0 },
        'LONDON': { pnl: 0, trades: 0, wins: 0, rr: 0 },
        'NEW_YORK': { pnl: 0, trades: 0, wins: 0, rr: 0 }
    };
    
    filteredTrades.forEach(trade => {
        if (!trade.session || !sessionStats[trade.session]) return;
        sessionStats[trade.session].pnl += trade.profit_loss || 0;
        sessionStats[trade.session].trades += 1;
        if (trade.result === 'WIN') sessionStats[trade.session].wins += 1;
        if (trade.rr_obtained) sessionStats[trade.session].rr += trade.rr_obtained;
    });
    
    const options = {
        series: [
            { name: 'Win Rate (%)', data: Object.values(sessionStats).map(s => s.trades > 0 ? (s.wins / s.trades * 100) : 0) },
            { name: 'RR Moyen', data: Object.values(sessionStats).map(s => s.trades > 0 ? (s.rr / s.trades) : 0) }
        ],
        chart: {
            type: 'bar',
            height: 350,
            fontFamily: 'Inter, sans-serif',
            background: 'transparent',
            toolbar: { show: false }
        },
        colors: ['#00D26A', '#3B82F6'],
        plotOptions: {
            bar: { borderRadius: 4, columnWidth: '50%' }
        },
        xaxis: {
            categories: Object.keys(sessionStats),
            labels: { style: { colors: '#8B9AB1', fontSize: '12px' } }
        },
        yaxis: {
            labels: { style: { colors: '#8B9AB1', fontSize: '12px' } }
        },
        grid: { borderColor: '#1E2330', strokeDashArray: 4 },
        tooltip: { theme: 'dark' }
    };
    
    charts.sessionPerformanceChart = new ApexCharts(document.getElementById('sessionPerformanceChart'), options);
    charts.sessionPerformanceChart.render();
}

/**
 * Render Performance by Asset Chart
 */
function renderAssetPerformanceChart() {
    if (charts.assetPerformanceChart) charts.assetPerformanceChart.destroy();
    
    const assetStats = {};
    filteredTrades.forEach(trade => {
        if (!assetStats[trade.asset]) {
            assetStats[trade.asset] = { pnl: 0, trades: 0, wins: 0 };
        }
        assetStats[trade.asset].pnl += trade.profit_loss || 0;
        assetStats[trade.asset].trades += 1;
        if (trade.result === 'WIN') assetStats[trade.asset].wins += 1;
    });
    
    const sortedAssets = Object.entries(assetStats)
        .sort((a, b) => b[1].pnl - a[1].pnl);
    
    const options = {
        series: [{
            data: sortedAssets.map(([_, stats]) => stats.pnl)
        }],
        chart: {
            type: 'bar',
            height: 350,
            fontFamily: 'Inter, sans-serif',
            background: 'transparent',
            toolbar: { show: false }
        },
        plotOptions: {
            bar: {
                borderRadius: 4,
                horizontal: true,
                barHeight: '60%'
            }
        },
        colors: sortedAssets.map(([_, stats]) => {
            const wr = (stats.wins / stats.trades * 100);
            if (wr >= 60) return '#00D26A';
            if (wr >= 40) return '#F59E0B';
            return '#FF4757';
        }),
        xaxis: {
            categories: sortedAssets.map(([asset, _]) => asset),
            labels: { style: { colors: '#8B9AB1', fontSize: '12px' } }
        },
        yaxis: {
            labels: {
                style: { colors: '#8B9AB1', fontSize: '12px' },
                formatter: (value) => formatCurrency(value)
            }
        },
        grid: { borderColor: '#1E2330', strokeDashArray: 4 },
        tooltip: {
            theme: 'dark',
            y: { formatter: (value) => formatCurrency(value) },
            custom: ({ series, seriesIndex, dataPointIndex, w }) => {
                const [asset, stats] = sortedAssets[dataPointIndex];
                const wr = (stats.wins / stats.trades * 100).toFixed(1);
                return `<div>${asset}<br>WR: ${wr}%<br>P&L: ${formatCurrency(stats.pnl)}<br>Trades: ${stats.trades}</div>`;
            }
        }
    };
    
    charts.assetPerformanceChart = new ApexCharts(document.getElementById('assetPerformanceChart'), options);
    charts.assetPerformanceChart.render();
}

/**
 * Render Trading Score Evolution Chart
 */
function renderTradingScoreChart() {
    if (charts.tradingScoreChart) charts.tradingScoreChart.destroy();
    
    const sortedTrades = [...filteredTrades].sort((a, b) => new Date(a.trade_date) - new Date(b.trade_date));
    
    // Calculate weekly averages
    const weeklyScores = {};
    sortedTrades.forEach(trade => {
        if (!trade.trading_score) return;
        const week = getWeekNumber(new Date(trade.trade_date));
        if (!weeklyScores[week]) weeklyScores[week] = { total: 0, count: 0 };
        weeklyScores[week].total += trade.trading_score;
        weeklyScores[week].count += 1;
    });
    
    const weeks = Object.keys(weeklyScores).sort();
    const avgScores = weeks.map(w => weeklyScores[w].total / weeklyScores[w].count);
    
    const options = {
        series: [{
            name: 'Score Moyen',
            data: avgScores
        }],
        chart: {
            type: 'line',
            height: 350,
            fontFamily: 'Inter, sans-serif',
            background: 'transparent',
            toolbar: { show: false }
        },
        colors: ['#8B5CF6'],
        stroke: { curve: 'smooth', width: 2 },
        xaxis: {
            categories: weeks,
            labels: { style: { colors: '#8B9AB1', fontSize: '12px' } }
        },
        yaxis: {
            min: 0,
            max: 100,
            labels: { style: { colors: '#8B9AB1', fontSize: '12px' } }
        },
        grid: { borderColor: '#1E2330', strokeDashArray: 4 },
        tooltip: { theme: 'dark' }
    };
    
    charts.tradingScoreChart = new ApexCharts(document.getElementById('tradingScoreChart'), options);
    charts.tradingScoreChart.render();
}

/**
 * Render RR Distribution Chart
 */
function renderRRDistributionChart() {
    if (charts.rrDistributionChart) charts.rrDistributionChart.destroy();
    
    const rrValues = filteredTrades
        .filter(t => t.rr_obtained !== null && t.rr_obtained !== undefined)
        .map(t => t.rr_obtained);
    
    const avgRR = rrValues.reduce((sum, val) => sum + val, 0) / rrValues.length;
    
    // Create histogram bins
    const bins = {};
    rrValues.forEach(rr => {
        const bin = Math.floor(rr);
        if (!bins[bin]) bins[bin] = 0;
        bins[bin]++;
    });
    
    const sortedBins = Object.keys(bins).sort((a, b) => parseInt(a) - parseInt(b));
    
    const options = {
        series: [{
            data: sortedBins.map(bin => bins[bin])
        }],
        chart: {
            type: 'bar',
            height: 350,
            fontFamily: 'Inter, sans-serif',
            background: 'transparent',
            toolbar: { show: false }
        },
        colors: sortedBins.map(bin => parseInt(bin) >= 0 ? '#00D26A' : '#FF4757'),
        plotOptions: {
            bar: { borderRadius: 4, columnWidth: '80%' }
        },
        xaxis: {
            categories: sortedBins,
            labels: { style: { colors: '#8B9AB1', fontSize: '12px' } },
            title: { text: 'RR', style: { color: '#8B9AB1' } }
        },
        yaxis: {
            labels: { style: { colors: '#8B9AB1', fontSize: '12px' } },
            title: { text: 'Nombre de trades', style: { color: '#8B9AB1' } }
        },
        grid: { borderColor: '#1E2330', strokeDashArray: 4 },
        annotations: {
            xaxis: [{
                x: avgRR,
                borderColor: '#8B5CF6',
                label: { style: { color: '#8B5CF6' }, text: `Moyen: ${avgRR.toFixed(2)}` }
            }]
        },
        tooltip: { theme: 'dark' }
    };
    
    charts.rrDistributionChart = new ApexCharts(document.getElementById('rrDistributionChart'), options);
    charts.rrDistributionChart.render();
}

/**
 * Render Confidence/Performance Correlation Chart
 */
function renderConfidenceCorrelationChart() {
    if (charts.confidenceCorrelationChart) charts.confidenceCorrelationChart.destroy();
    
    const data = filteredTrades
        .filter(t => t.confidence_level !== null && t.confidence_level !== undefined && t.profit_loss !== null)
        .map(t => ({
            x: t.confidence_level,
            y: t.profit_loss,
            result: t.result
        }));
    
    const options = {
        series: [{
            name: 'Trades',
            data: data
        }],
        chart: {
            type: 'scatter',
            height: 350,
            fontFamily: 'Inter, sans-serif',
            background: 'transparent',
            toolbar: { show: false }
        },
        colors: data.map(d => d.result === 'WIN' ? '#00D26A' : '#FF4757'),
        xaxis: {
            type: 'numeric',
            min: 1,
            max: 10,
            title: { text: 'Confiance (1-10)', style: { color: '#8B9AB1' } },
            labels: { style: { colors: '#8B9AB1', fontSize: '12px' } }
        },
        yaxis: {
            title: { text: 'P&L ($)', style: { color: '#8B9AB1' } },
            labels: {
                style: { colors: '#8B9AB1', fontSize: '12px' },
                formatter: (value) => formatCurrency(value)
            }
        },
        grid: { borderColor: '#1E2330', strokeDashArray: 4 },
        tooltip: {
            theme: 'dark',
            x: { formatter: (value) => `Confiance: ${value}/10` },
            y: { formatter: (value) => formatCurrency(value) }
        },
        markers: { size: 8 }
    };
    
    charts.confidenceCorrelationChart = new ApexCharts(document.getElementById('confidenceCorrelationChart'), options);
    charts.confidenceCorrelationChart.render();
}

/**
 * Render Heatmap
 */
function renderHeatmap() {
    const grid = document.getElementById('heatmapGrid');
    grid.innerHTML = '';
    
    const days = ['', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'];
    
    // Header row
    days.forEach(day => {
        const label = document.createElement('div');
        label.className = 'heatmap-label';
        label.textContent = day;
        grid.appendChild(label);
    });
    
    // Hour labels and cells
    for (let hour = 0; hour < 24; hour++) {
        const hourLabel = document.createElement('div');
        hourLabel.className = 'heatmap-label';
        hourLabel.textContent = hour;
        grid.appendChild(hourLabel);
        
        for (let day = 1; day <= 7; day++) {
            const cell = document.createElement('div');
            cell.className = 'heatmap-cell';
            
            // Calculate performance for this hour/day
            let totalPnL = 0;
            let totalTrades = 0;
            let totalWins = 0;
            
            filteredTrades.forEach(trade => {
                if (trade.entry_time) {
                    const entryDate = new Date(trade.entry_time);
                    const entryHour = entryDate.getHours();
                    const entryDay = entryDate.getDay();
                    
                    if (entryHour === hour && entryDay === (day === 7 ? 0 : day)) {
                        totalPnL += trade.profit_loss || 0;
                        totalTrades += 1;
                        if (trade.result === 'WIN') totalWins += 1;
                    }
                }
            });
            
            if (totalTrades > 0) {
                const avgPnL = totalPnL / totalTrades;
                const winRate = (totalWins / totalTrades * 100);
                
                // Set color based on P&L
                const intensity = Math.min(Math.abs(avgPnL) / 200, 1);
                if (avgPnL > 50) {
                    cell.style.background = `rgba(0, 210, 106, ${0.3 + intensity * 0.7})`;
                } else if (avgPnL > 0) {
                    cell.style.background = `rgba(0, 210, 106, ${0.1 + intensity * 0.2})`;
                } else if (avgPnL < -50) {
                    cell.style.background = `rgba(255, 71, 87, ${0.3 + intensity * 0.7})`;
                } else if (avgPnL < 0) {
                    cell.style.background = `rgba(255, 71, 87, ${0.1 + intensity * 0.2})`;
                } else {
                    cell.style.background = 'var(--bg-secondary)';
                }
                
                // Tooltip
                cell.addEventListener('mouseenter', (e) => {
                    showTooltip(e, `${days[day]} ${hour}h: ${totalTrades} trades, Win Rate ${winRate.toFixed(0)}%, P&L moyen ${formatCurrency(avgPnL)}`);
                });
                
                cell.addEventListener('mouseleave', hideTooltip);
            } else {
                cell.style.background = 'var(--bg-secondary)';
            }
            
            grid.appendChild(cell);
        }
    }
}

/**
 * Render Stats Table
 */
function renderStatsTable() {
    const tbody = document.getElementById('statsTableBody');
    
    const calculateStats = (trades) => {
        if (trades.length === 0) return { winRate: 0, avgPnL: 0, avgRR: 0, profitFactor: 0, count: 0 };
        
        const wins = trades.filter(t => t.result === 'WIN');
        const losses = trades.filter(t => t.result === 'LOSS');
        
        const winRate = (wins.length / trades.length * 100);
        const avgPnL = trades.reduce((sum, t) => sum + (t.profit_loss || 0), 0) / trades.length;
        const avgRR = trades.filter(t => t.rr_obtained).reduce((sum, t) => sum + t.rr_obtained, 0) / trades.filter(t => t.rr_obtained).length || 0;
        
        const totalWinsPnL = wins.reduce((sum, t) => sum + (t.profit_loss || 0), 0);
        const totalLossesPnL = Math.abs(losses.reduce((sum, t) => sum + (t.profit_loss || 0), 0));
        const profitFactor = totalLossesPnL > 0 ? totalWinsPnL / totalLossesPnL : 0;
        
        return { winRate, avgPnL, avgRR, profitFactor, count: trades.length };
    };
    
    const globalStats = calculateStats(filteredTrades);
    const buyStats = calculateStats(filteredTrades.filter(t => t.direction === 'BUY'));
    const sellStats = calculateStats(filteredTrades.filter(t => t.direction === 'SELL'));
    const asiaStats = calculateStats(filteredTrades.filter(t => t.session === 'ASIA'));
    const londonStats = calculateStats(filteredTrades.filter(t => t.session === 'LONDON'));
    const nyStats = calculateStats(filteredTrades.filter(t => t.session === 'NEW_YORK'));
    
    const metrics = [
        { name: 'Win Rate', format: v => `${v.toFixed(1)}%` },
        { name: 'P&L Moyen', format: v => formatCurrency(v) },
        { name: 'RR Moyen', format: v => v.toFixed(2) },
        { name: 'Profit Factor', format: v => v.toFixed(2) },
        { name: 'Nb Trades', format: v => v }
    ];
    
    tbody.innerHTML = metrics.map(metric => {
        const formatValue = (stats) => {
            const value = stats[metric.name.toLowerCase().replace(' ', '')] || stats[metric.name.toLowerCase().replace(' ', '_')] || 0;
            const formatted = metric.format(value);
            const isPositive = metric.name === 'Win Rate' ? value >= 50 : value >= 0;
            return `<span class="${isPositive ? 'positive' : 'negative'}">${formatted}</span>`;
        };
        
        return `
            <tr>
                <td><strong>${metric.name}</strong></td>
                <td>${formatValue(globalStats)}</td>
                <td>${formatValue(buyStats)}</td>
                <td>${formatValue(sellStats)}</td>
                <td>${formatValue(asiaStats)}</td>
                <td>${formatValue(londonStats)}</td>
                <td>${formatValue(nyStats)}</td>
            </tr>
        `;
    }).join('');
}

/**
 * Toggle comparison mode
 */
function toggleComparisonMode() {
    comparisonMode = !comparisonMode;
    document.getElementById('comparisonMode').style.display = comparisonMode ? 'flex' : 'none';
    
    if (comparisonMode) {
        updateComparisonCharts();
    }
}

/**
 * Update comparison charts
 */
function updateComparisonCharts() {
    if (!comparisonMode) return;
    
    const period1 = document.getElementById('comparisonPeriod1').value;
    const period2 = document.getElementById('comparisonPeriod2').value;
    
    // Filter trades for each period
    const filterByPeriod = (trades, period) => {
        const periodMap = { '7d': 7, '30d': 30, '90d': 90 };
        const days = periodMap[period] || 30;
        const cutoff = new Date(new Date() - days * 24 * 60 * 60 * 1000);
        return trades.filter(t => new Date(t.trade_date) >= cutoff);
    };
    
    const trades1 = filterByPeriod(allTrades, period1);
    const trades2 = filterByPeriod(allTrades, period2);
    
    // Render comparison charts
    renderComparisonChart('comparisonChart1', trades1, period1);
    renderComparisonChart('comparisonChart2', trades2, period2);
}

/**
 * Render comparison chart
 */
function renderComparisonChart(elementId, trades, period) {
    if (charts[elementId]) charts[elementId].destroy();
    
    const sortedTrades = [...trades].sort((a, b) => new Date(a.trade_date) - new Date(b.trade_date));
    let cumulative = 0;
    const equityData = sortedTrades.map(trade => {
        cumulative += trade.profit_loss || 0;
        return {
            x: new Date(trade.trade_date).getTime(),
            y: cumulative
        };
    });
    
    const options = {
        series: [{ name: 'Équité', data: equityData }],
        chart: {
            type: 'area',
            height: 300,
            fontFamily: 'Inter, sans-serif',
            background: 'transparent',
            toolbar: { show: false }
        },
        colors: ['#3B82F6'],
        fill: { type: 'gradient', gradient: { shadeIntensity: 1, opacityFrom: 0.7, opacityTo: 0.1, stops: [0, 90, 100] } },
        xaxis: { type: 'datetime', labels: { style: { colors: '#8B9AB1', fontSize: '12px' } } },
        yaxis: { labels: { style: { colors: '#8B9AB1', fontSize: '12px' }, formatter: (value) => formatCurrency(value) } },
        grid: { borderColor: '#1E2330', strokeDashArray: 4 },
        tooltip: { theme: 'dark', y: { formatter: (value) => formatCurrency(value) } }
    };
    
    charts[elementId] = new ApexCharts(document.getElementById(elementId), options);
    charts[elementId].render();
}

/**
 * Export stats as JSON
 */
function exportStats() {
    const exportData = {
        period: document.getElementById('periodFilter').value,
        filters: {
            account: document.getElementById('accountFilter').value,
            asset: document.getElementById('assetFilter').value,
            setup: document.getElementById('setupFilter').value,
            session: document.getElementById('sessionFilter').value
        },
        trades: filteredTrades,
        summary: {
            totalTrades: filteredTrades.length,
            totalPnL: filteredTrades.reduce((sum, t) => sum + (t.profit_loss || 0), 0),
            winRate: (filteredTrades.filter(t => t.result === 'WIN').length / filteredTrades.length * 100).toFixed(1)
        }
    };
    
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `smartreview_stats_${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
    
    showToast('Statistiques exportées avec succès', 'success');
}

/**
 * Get week number
 */
function getWeekNumber(date) {
    const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
    const dayNum = d.getUTCDay() || 7;
    d.setUTCDate(d.getUTCDate() + 4 - dayNum);
    const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
}

/**
 * Show tooltip
 */
function showTooltip(e, text) {
    const tooltip = document.createElement('div');
    tooltip.className = 'heatmap-tooltip';
    tooltip.textContent = text;
    tooltip.style.position = 'fixed';
    tooltip.style.left = `${e.clientX + 10}px`;
    tooltip.style.top = `${e.clientY + 10}px`;
    tooltip.style.background = 'var(--bg-card)';
    tooltip.style.color = 'var(--text-primary)';
    tooltip.style.padding = '8px 12px';
    tooltip.style.borderRadius = '4px';
    tooltip.style.fontSize = '12px';
    tooltip.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.3)';
    tooltip.style.zIndex = '1000';
    tooltip.id = 'heatmapTooltip';
    document.body.appendChild(tooltip);
}

/**
 * Hide tooltip
 */
function hideTooltip() {
    const tooltip = document.getElementById('heatmapTooltip');
    if (tooltip) tooltip.remove();
}

/**
 * Handle account change
 */
function onAccountChange(accountId) {
    loadTrades().then(() => {
        populateFilters();
        applyFilters();
    });
}

// Initialize when layout is ready
document.addEventListener('layout-ready', initializeStats);
document.addEventListener('DOMContentLoaded', () => {
    if (!document.getElementById('app-layout-root')) {
        initializeCommon();
        initializeStats();
    }
});
