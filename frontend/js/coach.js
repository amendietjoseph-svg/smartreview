/**
 * AI Coach functionality for SmartReview
 * Handles AI analysis, edge detection, reports, and streaming responses
 */

let allTrades = [];
let lastAnalysisTime = null;
let psychChart = null;
let analysisCooldown = false;

/**
 * Initialize AI Coach
 */
async function initializeCoach() {
    await loadTrades();
    setupEventListeners();
    checkLastAnalysis();
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

        const api = new API();
        allTrades = await api.getTrades(accountId);
        
        // Check if we have enough data to show the coach interface
        if (allTrades.length >= 5) {
            document.getElementById('onboardingCard').style.display = 'none';
            document.getElementById('analysisCard').style.display = 'block';
            document.getElementById('edgeTrackerCard').style.display = 'block';
            document.getElementById('reportsGrid').style.display = 'grid';
            document.getElementById('historySection').style.display = 'block';
            document.getElementById('psychSection').style.display = 'block';
            
            // Load initial data
            await loadEdgeTracker();
            await loadReports();
            await loadHistory();
            renderPsychChart();
        }
        
    } catch (error) {
        console.error('Error loading trades:', error);
    }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Analyze performance button
    document.getElementById('analyzePerformanceBtn').addEventListener('click', () => {
        analyzePerformance();
    });

    // Detect edge button
    document.getElementById('detectEdgeBtn').addEventListener('click', () => {
        loadEdgeTracker();
    });

    // Daily report button
    document.getElementById('dailyReportBtn').addEventListener('click', () => {
        loadReports();
    });

    // Refresh analysis button
    document.getElementById('refreshAnalysisBtn').addEventListener('click', () => {
        analyzePerformance();
    });

    // Copy analysis button
    document.getElementById('copyAnalysisBtn').addEventListener('click', () => {
        copyAnalysis();
    });

    // Period select change
    document.getElementById('periodSelect').addEventListener('change', () => {
        analyzePerformance();
    });

    // Account change
    const accountSelector = document.getElementById('activeAccount');
    if (accountSelector) {
        accountSelector.addEventListener('change', () => {
            loadTrades();
        });
    }
}

/**
 * Check last analysis time
 */
async function checkLastAnalysis() {
    try {
        const accountId = getActiveAccountId();
        if (!accountId) return;

        const api = new API();
        const response = await fetch(`${api.baseUrl}/ai/insights/${accountId}`);
        const data = await response.json();
        
        if (data.insights && data.insights.length > 0) {
            const lastAnalysis = data.insights[0];
            const analysisTime = new Date(lastAnalysis.created_at);
            const now = new Date();
            const hoursAgo = Math.floor((now - analysisTime) / (1000 * 60 * 60));
            
            if (hoursAgo < 1) {
                document.getElementById('lastAnalysisTime').textContent = 'Dernière analyse : il y a moins d\'une heure';
            } else if (hoursAgo < 24) {
                document.getElementById('lastAnalysisTime').textContent = `Dernière analyse : il y a ${hoursAgo} heure${hoursAgo > 1 ? 's' : ''}`;
            } else {
                document.getElementById('lastAnalysisTime').textContent = `Dernière analyse : il y a ${Math.floor(hoursAgo / 24)} jour${Math.floor(hoursAgo / 24) > 1 ? 's' : ''}`;
            }
            
            lastAnalysisTime = analysisTime;
        }
    } catch (error) {
        console.error('Error checking last analysis:', error);
    }
}

/**
 * Analyze performance with streaming
 */
async function analyzePerformance() {
    if (analysisCooldown) {
        showToast('Veuillez attendre avant de lancer une nouvelle analyse', 'warning');
        return;
    }

    const accountId = getActiveAccountId();
    if (!accountId) {
        showToast('Veuillez sélectionner un compte', 'error');
        return;
    }

    const period = document.getElementById('periodSelect').value;
    const analysisContent = document.getElementById('analysisContent');
    
    // Show loading state
    analysisContent.innerHTML = `
        <div class="loading-state">
            <div class="loading-dots">
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
            </div>
            <p class="loading-text">L'IA analyse vos performances...</p>
        </div>
    `;

    // Set cooldown
    analysisCooldown = true;
    setTimeout(() => { analysisCooldown = false; }, 30000);

    try {
        const api = new API();
        const response = await fetch(`${api.baseUrl}/ai/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                account_id: parseInt(accountId),
                period: period
            })
        });

        const data = await response.json();
        
        if (data.cached) {
            showToast('Analyse récupérée du cache (6h)', 'info');
        } else {
            showToast('Analyse générée avec succès', 'success');
        }

        // Render markdown
        analysisContent.innerHTML = `<div class="analysis-content markdown">${marked.parse(data.analysis)}</div>`;
        
        // Update last analysis time
        lastAnalysisTime = new Date();
        document.getElementById('lastAnalysisTime').textContent = 'Dernière analyse : à l\'instant';
        
        // Reload history
        await loadHistory();
        
    } catch (error) {
        console.error('Error analyzing performance:', error);
        analysisContent.innerHTML = `
            <div class="loading-state">
                <p class="loading-text" style="color: var(--accent-red);">Erreur lors de l'analyse</p>
                <p style="font-size: 13px; color: var(--text-muted);">${error.message}</p>
            </div>
        `;
        showToast('Erreur lors de l\'analyse', 'error');
    }
}

/**
 * Load edge tracker
 */
async function loadEdgeTracker() {
    try {
        const accountId = getActiveAccountId();
        if (!accountId) return;

        const api = new API();
        const response = await fetch(`${api.baseUrl}/ai/edge`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ account_id: parseInt(accountId) })
        });

        const data = await response.json();
        renderEdgeTracker(data.edges);
        
    } catch (error) {
        console.error('Error loading edge tracker:', error);
    }
}

/**
 * Render edge tracker
 */
function renderEdgeTracker(edges) {
    const edgeList = document.getElementById('edgeList');
    
    if (!edges || edges.length === 0) {
        edgeList.innerHTML = '<p style="color: var(--text-muted); text-align: center; padding: var(--spacing-lg);">Pas assez de données pour détecter des edges (min 5 trades par combinaison)</p>';
        return;
    }

    const ranks = ['gold', 'silver', 'bronze'];
    const medals = ['🥇', '🥈', '🥉'];
    
    edgeList.innerHTML = edges.slice(0, 3).map((edge, index) => {
        const dims = edge.dimensions;
        const combination = `${dims.asset} × ${dims.setup} × ${dims.session}`;
        const confidence = edge.composite_score;
        
        return `
            <div class="edge-item">
                <div class="edge-rank ${ranks[index]}">${medals[index]}</div>
                <div class="edge-details">
                    <div class="edge-combination">${combination}</div>
                    <div class="edge-stats">
                        <span class="edge-stat">
                            <i data-lucide="trending-up"></i>
                            WR: ${edge.win_rate.toFixed(1)}%
                        </span>
                        <span class="edge-stat">
                            <i data-lucide="target"></i>
                            RR: ${edge.avg_rr.toFixed(2)}
                        </span>
                        <span class="edge-stat">
                            <i data-lucide="dollar-sign"></i>
                            ${formatCurrency(edge.total_pnl)}
                        </span>
                        <span class="edge-stat">
                            <i data-lucide="activity"></i>
                            ${edge.total_trades} trades
                        </span>
                    </div>
                </div>
                <div class="edge-confidence">
                    <div class="edge-confidence-bar" style="width: ${confidence}%"></div>
                </div>
            </div>
        `;
    }).join('');
    
    lucide.createIcons();
}

/**
 * Load reports
 */
async function loadReports() {
    try {
        const accountId = getActiveAccountId();
        if (!accountId) return;

        const api = new API();
        
        // Daily report
        const dailyResponse = await fetch(`${api.baseUrl}/ai/daily-report`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ account_id: parseInt(accountId) })
        });
        const dailyData = await dailyResponse.json();
        document.getElementById('dailyReportContent').innerHTML = `<div class="report-content markdown">${marked.parse(dailyData.report)}</div>`;
        
        // Weekly summary
        const weeklyResponse = await fetch(`${api.baseUrl}/ai/weekly-summary`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ account_id: parseInt(accountId) })
        });
        const weeklyData = await weeklyResponse.json();
        document.getElementById('weeklyReportContent').innerHTML = `<div class="report-content markdown">${marked.parse(weeklyData.summary)}</div>`;
        
    } catch (error) {
        console.error('Error loading reports:', error);
    }
}

/**
 * Load analysis history
 */
async function loadHistory() {
    try {
        const accountId = getActiveAccountId();
        if (!accountId) return;

        const api = new API();
        const response = await fetch(`${api.baseUrl}/ai/insights/${accountId}`);
        const data = await response.json();
        
        renderHistory(data.insights);
        
    } catch (error) {
        console.error('Error loading history:', error);
    }
}

/**
 * Render history timeline
 */
function renderHistory(insights) {
    const timeline = document.getElementById('historyTimeline');
    
    if (!insights || insights.length === 0) {
        timeline.innerHTML = '<p style="color: var(--text-muted);">Aucune analyse précédente</p>';
        return;
    }

    timeline.innerHTML = insights.map(insight => {
        const date = new Date(insight.created_at);
        const dateStr = date.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric' });
        const timeStr = date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
        
        // Get first line of content as summary
        const summary = insight.content.split('\n')[1] || insight.content.substring(0, 100);
        
        return `
            <div class="history-item" onclick="showHistoryAnalysis(${insight.id})">
                <div class="history-date">
                    ${dateStr}<br>${timeStr}
                </div>
                <div class="history-summary">${summary}</div>
            </div>
        `;
    }).join('');
}

/**
 * Show history analysis
 */
async function showHistoryAnalysis(analysisId) {
    try {
        const accountId = getActiveAccountId();
        const api = new API();
        const response = await fetch(`${api.baseUrl}/ai/insights/${accountId}`);
        const data = await response.json();
        
        const analysis = data.insights.find(a => a.id === analysisId);
        if (analysis) {
            const analysisContent = document.getElementById('analysisContent');
            analysisContent.innerHTML = `<div class="analysis-content markdown">${marked.parse(analysis.content)}</div>`;
            
            // Scroll to analysis
            document.getElementById('analysisCard').scrollIntoView({ behavior: 'smooth' });
        }
    } catch (error) {
        console.error('Error showing history analysis:', error);
    }
}

/**
 * Render psychological correlations chart
 */
function renderPsychChart() {
    if (!allTrades || allTrades.length === 0) return;

    // Map emotional states to numeric values
    emotionMap = {
        'très stressé': 1,
        'stressé': 2,
        'tendu': 3,
        'neutre': 5,
        'calme': 7,
        'très calme': 8,
        'confiant': 9,
        'zen': 10
    };

    const chartData = allTrades.map(trade => {
        const emotionValue = emotionMap[trade.emotional_state] || 5;
        return {
            x: emotionValue,
            y: trade.profit_loss,
            result: trade.result
        };
    });

    const options = {
        series: [{
            name: 'Trades',
            data: chartData
        }],
        chart: {
            type: 'scatter',
            height: 400,
            fontFamily: 'Inter, sans-serif',
            background: 'transparent',
            toolbar: { show: false }
        },
        colors: chartData.map(d => d.result === 'WIN' ? '#00D26A' : '#FF4757'),
        xaxis: {
            type: 'numeric',
            min: 0,
            max: 10,
            title: {
                text: 'État Émotionnel (1=Stressé → 10=Calme)',
                style: { color: '#8B9AB1', fontSize: '12px' }
            },
            labels: {
                style: { colors: '#8B9AB1', fontSize: '12px' }
            }
        },
        yaxis: {
            title: {
                text: 'P&L ($)',
                style: { color: '#8B9AB1', fontSize: '12px' }
            },
            labels: {
                style: { colors: '#8B9AB1', fontSize: '12px' },
                formatter: (value) => formatCurrency(value)
            }
        },
        grid: { borderColor: '#1E2330', strokeDashArray: 4 },
        tooltip: {
            theme: 'dark',
            x: { formatter: (value) => `État: ${value}/10` },
            y: { formatter: (value) => formatCurrency(value) }
        },
        markers: {
            size: 8
        }
    };

    if (psychChart) psychChart.destroy();
    psychChart = new ApexCharts(document.getElementById('psychChart'), options);
    psychChart.render();

    // Generate insight
    generatePsychInsight(chartData);
}

/**
 * Generate psychological insight
 */
function generatePsychInsight(chartData) {
    if (!chartData || chartData.length === 0) return;

    // Calculate average P&L by emotion level
    const emotionGroups = {};
    chartData.forEach(d => {
        if (!emotionGroups[d.x]) {
            emotionGroups[d.x] = { total: 0, count: 0 };
        }
        emotionGroups[d.x].total += d.y;
        emotionGroups[d.x].count += 1;
    });

    let bestEmotion = null;
    let bestAvgPnL = -Infinity;

    Object.keys(emotionGroups).forEach(emotion => {
        const avgPnL = emotionGroups[emotion].total / emotionGroups[emotion].count;
        if (avgPnL > bestAvgPnL) {
            bestAvgPnL = avgPnL;
            bestEmotion = parseInt(emotion);
        }
    });

    const emotionLabels = {
        1: 'très stressé',
        2: 'stressé',
        3: 'tendu',
        5: 'neutre',
        7: 'calme',
        8: 'très calme',
        9: 'confiant',
        10: 'zen'
    };

    const insight = document.getElementById('psychInsight');
    if (bestEmotion) {
        insight.innerHTML = `
            <strong>💡 Insight automatique :</strong> 
            Vos meilleures performances surviennent quand vous êtes 
            <span style="color: var(--accent-green); font-weight: 600;">${emotionLabels[bestEmotion] || bestEmotion}</span>
            (${bestEmotion}/10).
            P&L moyen dans cet état : ${formatCurrency(bestAvgPnL)}.
        `;
    } else {
        insight.innerHTML = '<strong>💡 Insight :</strong> Pas assez de données pour générer un insight.';
    }
}

/**
 * Copy analysis to clipboard
 */
function copyAnalysis() {
    const analysisContent = document.getElementById('analysisContent');
    const text = analysisContent.innerText;
    
    navigator.clipboard.writeText(text).then(() => {
        showToast('Analyse copiée dans le presse-papier', 'success');
    }).catch(err => {
        showToast('Erreur lors de la copie', 'error');
    });
}

/**
 * Handle account change
 */
function onAccountChange(accountId) {
    loadTrades();
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    initializeCommon();
    initializeCoach();
});
