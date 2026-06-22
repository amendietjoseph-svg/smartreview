/**
 * Calendar functionality for SmartReview
 * Handles month, week, and year views, heatmaps, statistics, and day details
 */

let currentDate = new Date();
let currentView = 'month';
let allTrades = [];
let tradesByDate = {};
let pnlChart = null;
let winRateChart = null;

const monthNames = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
                   'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'];
const dayNames = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'];

/**
 * Initialize calendar
 */
async function initializeCalendar() {
    await loadTrades();
    setupEventListeners();
    renderCurrentView();
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
        groupTradesByDate();
        
    } catch (error) {
        console.error('Error loading trades:', error);
        showToast('Erreur de chargement des trades', 'error');
    }
}

/**
 * Group trades by date
 */
function groupTradesByDate() {
    tradesByDate = {};
    
    allTrades.forEach(trade => {
        if (!trade.trade_date) return;
        
        const dateKey = trade.trade_date.split('T')[0];
        if (!tradesByDate[dateKey]) {
            tradesByDate[dateKey] = [];
        }
        tradesByDate[dateKey].push(trade);
    });
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // View buttons
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentView = btn.dataset.view;
            renderCurrentView();
        });
    });

    // Period navigation
    document.getElementById('prevPeriod').addEventListener('click', () => {
        navigatePeriod(-1);
    });

    document.getElementById('nextPeriod').addEventListener('click', () => {
        navigatePeriod(1);
    });

    // Detail panel close
    document.getElementById('closeDetailPanel').addEventListener('click', () => {
        document.getElementById('dayDetailPanel').classList.remove('active');
    });

    // Account change
    const accountSelector = document.getElementById('activeAccount');
    if (accountSelector) {
        accountSelector.addEventListener('change', () => {
            loadTrades().then(() => renderCurrentView());
        });
    }
}

/**
 * Navigate period based on current view
 */
function navigatePeriod(direction) {
    if (currentView === 'month') {
        currentDate.setMonth(currentDate.getMonth() + direction);
    } else if (currentView === 'week') {
        currentDate.setDate(currentDate.getDate() + (direction * 7));
    } else if (currentView === 'year') {
        currentDate.setFullYear(currentDate.getFullYear() + direction);
    }
    renderCurrentView();
}

/**
 * Render current view
 */
function renderCurrentView() {
    switch (currentView) {
        case 'month':
            renderMonthView();
            break;
        case 'week':
            renderWeekView();
            break;
        case 'year':
            renderYearView();
            break;
    }
    
    updatePeriodLabel();
    updateMonthStats();
    renderHeatmap();
    renderBestWorstDays();
    renderMonthlyStats();
}

/**
 * Update period label
 */
function updatePeriodLabel() {
    const label = document.getElementById('currentPeriodLabel');
    
    if (currentView === 'month') {
        label.textContent = `${monthNames[currentDate.getMonth()]} ${currentDate.getFullYear()}`;
    } else if (currentView === 'week') {
        const weekStart = getWeekStart(currentDate);
        const weekEnd = new Date(weekStart);
        weekEnd.setDate(weekEnd.getDate() + 6);
        label.textContent = `${formatDate(weekStart)} - ${formatDate(weekEnd)}`;
    } else if (currentView === 'year') {
        label.textContent = `${currentDate.getFullYear()}`;
    }
}

/**
 * Get week start (Monday)
 */
function getWeekStart(date) {
    const d = new Date(date);
    const day = d.getDay();
    const diff = d.getDate() - day + (day === 0 ? -6 : 1);
    return new Date(d.setDate(diff));
}

/**
 * Render month view
 */
function renderMonthView() {
    document.getElementById('monthView').classList.add('active');
    document.getElementById('weekView').classList.remove('active');
    document.getElementById('yearView').classList.remove('active');
    
    const grid = document.getElementById('calendarGrid');
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    
    const firstDay = new Date(year, month, 1);
    const startDay = firstDay.getDay() === 0 ? 6 : firstDay.getDay() - 1; // Monday = 0
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    
    grid.innerHTML = '';
    
    // Empty cells for days before first day
    for (let i = 0; i < startDay; i++) {
        const cell = document.createElement('div');
        cell.className = 'calendar-day empty';
        grid.appendChild(cell);
    }
    
    // Days of the month
    for (let day = 1; day <= daysInMonth; day++) {
        const cell = document.createElement('div');
        cell.className = 'calendar-day';
        
        const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        const today = new Date();
        const cellDate = new Date(year, month, day);
        
        // Check if today
        if (cellDate.toDateString() === today.toDateString()) {
            cell.classList.add('current');
        }
        
        // Check if future
        if (cellDate > today) {
            cell.classList.add('future');
        }
        
        const dayNumber = document.createElement('div');
        dayNumber.className = 'calendar-day-number';
        dayNumber.textContent = day;
        cell.appendChild(dayNumber);
        
        // Check if there are trades on this day
        const dayTrades = tradesByDate[dateStr] || [];
        if (dayTrades.length > 0) {
            const dayPnL = dayTrades.reduce((sum, t) => sum + (t.profit_loss || 0), 0);
            const wins = dayTrades.filter(t => t.result === 'WIN').length;
            const winRate = (wins / dayTrades.length * 100).toFixed(0);
            
            // Set background color based on P&L
            const intensity = Math.min(Math.abs(dayPnL) / 500, 1);
            if (dayPnL > 0) {
                cell.style.background = `rgba(0, 210, 106, ${0.1 + intensity * 0.3})`;
            } else if (dayPnL < 0) {
                cell.style.background = `rgba(255, 71, 87, ${0.1 + intensity * 0.3})`;
            }
            
            const pnl = document.createElement('div');
            pnl.className = `day-pnl ${dayPnL >= 0 ? 'positive' : 'negative'}`;
            pnl.textContent = formatCurrency(dayPnL);
            cell.appendChild(pnl);
            
            const tradesCount = document.createElement('div');
            tradesCount.className = 'day-trades-count';
            tradesCount.textContent = `${dayTrades.length} trades`;
            cell.appendChild(tradesCount);
            
            const winRateBadge = document.createElement('span');
            winRateBadge.className = `day-winrate-badge ${getWinRateClass(winRate)}`;
            winRateBadge.textContent = `${winRate}%`;
            cell.appendChild(winRateBadge);
        }
        
        cell.addEventListener('click', () => showDayDetails(dateStr, dayTrades));
        grid.appendChild(cell);
    }
}

/**
 * Get win rate class
 */
function getWinRateClass(winRate) {
    if (winRate >= 70) return 'high';
    if (winRate >= 50) return 'medium';
    return 'low';
}

/**
 * Render week view
 */
function renderWeekView() {
    document.getElementById('monthView').classList.remove('active');
    document.getElementById('weekView').classList.add('active');
    document.getElementById('yearView').classList.remove('active');
    
    const timeline = document.getElementById('weekTimeline');
    const weekStart = getWeekStart(currentDate);
    
    timeline.innerHTML = '';
    
    for (let i = 0; i < 7; i++) {
        const dayDate = new Date(weekStart);
        dayDate.setDate(dayDate.getDate() + i);
        const dateStr = dayDate.toISOString().split('T')[0];
        const dayTrades = tradesByDate[dateStr] || [];
        
        const column = document.createElement('div');
        column.className = 'week-day-column';
        
        const header = document.createElement('div');
        header.className = 'week-day-header';
        header.textContent = `${dayNames[dayDate.getDay()]} ${dayDate.getDate()}`;
        column.appendChild(header);
        
        dayTrades.forEach(trade => {
            const tradeItem = document.createElement('div');
            tradeItem.className = 'week-trade-item';
            tradeItem.innerHTML = `
                <div style="font-weight: 600;">${trade.asset}</div>
                <div>${trade.direction} | ${formatCurrency(trade.profit_loss)}</div>
            `;
            tradeItem.addEventListener('click', () => {
                window.location.href = `journal.html`;
            });
            column.appendChild(tradeItem);
        });
        
        timeline.appendChild(column);
    }
}

/**
 * Render year view
 */
function renderYearView() {
    document.getElementById('monthView').classList.remove('active');
    document.getElementById('weekView').classList.remove('active');
    document.getElementById('yearView').classList.add('active');
    
    const grid = document.getElementById('yearGrid');
    const year = currentDate.getFullYear();
    
    grid.innerHTML = '';
    
    for (let month = 0; month < 12; month++) {
        const monthCell = document.createElement('div');
        monthCell.className = 'year-month';
        
        const monthName = document.createElement('div');
        monthName.className = 'year-month-name';
        monthName.textContent = monthNames[month];
        monthCell.appendChild(monthName);
        
        // Calculate month stats
        let monthPnL = 0;
        let monthTrades = 0;
        
        for (let day = 1; day <= 31; day++) {
            const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            const dayTrades = tradesByDate[dateStr] || [];
            monthTrades += dayTrades.length;
            monthPnL += dayTrades.reduce((sum, t) => sum + (t.profit_loss || 0), 0);
        }
        
        const stats = document.createElement('div');
        stats.className = 'year-month-stats';
        stats.textContent = `${monthTrades} trades`;
        monthCell.appendChild(stats);
        
        const pnl = document.createElement('div');
        pnl.className = `year-month-pnl ${monthPnL >= 0 ? 'positive' : 'negative'}`;
        pnl.textContent = formatCurrency(monthPnL);
        monthCell.appendChild(pnl);
        
        monthCell.addEventListener('click', () => {
            currentDate = new Date(year, month, 1);
            currentView = 'month';
            document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
            document.querySelector('.view-btn[data-view="month"]').classList.add('active');
            renderCurrentView();
        });
        
        grid.appendChild(monthCell);
    }
}

/**
 * Update month stats
 */
function updateMonthStats() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    
    let monthPnL = 0;
    let monthWins = 0;
    let monthTrades = 0;
    let tradedDays = 0;
    let bestDay = { date: null, pnl: -Infinity };
    let worstDay = { date: null, pnl: Infinity };
    
    for (let day = 1; day <= 31; day++) {
        const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        const dayTrades = tradesByDate[dateStr] || [];
        
        if (dayTrades.length > 0) {
            tradedDays++;
            const dayPnL = dayTrades.reduce((sum, t) => sum + (t.profit_loss || 0), 0);
            monthPnL += dayPnL;
            monthTrades += dayTrades.length;
            monthWins += dayTrades.filter(t => t.result === 'WIN').length;
            
            if (dayPnL > bestDay.pnl) {
                bestDay = { date: dateStr, pnl: dayPnL };
            }
            if (dayPnL < worstDay.pnl) {
                worstDay = { date: dateStr, pnl: dayPnL };
            }
        }
    }
    
    const monthWinRate = monthTrades > 0 ? (monthWins / monthTrades * 100).toFixed(1) : 0;
    
    document.getElementById('monthPnL').textContent = formatCurrency(monthPnL);
    document.getElementById('monthPnL').className = `month-stat-value ${monthPnL >= 0 ? 'positive' : 'negative'}`;
    document.getElementById('monthWinRate').textContent = `${monthWinRate}%`;
    document.getElementById('monthTradedDays').textContent = tradedDays;
    document.getElementById('monthBestDay').textContent = bestDay.date ? `${formatDate(bestDay.date)} (${formatCurrency(bestDay.pnl)})` : '--';
    document.getElementById('monthWorstDay').textContent = worstDay.date ? `${formatDate(worstDay.date)} (${formatCurrency(worstDay.pnl)})` : '--';
}

/**
 * Render heatmap
 */
function renderHeatmap() {
    const grid = document.getElementById('heatmapGrid');
    grid.innerHTML = '';
    
    const days = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'];
    
    for (let day = 0; day < 7; day++) {
        for (let hour = 0; hour < 24; hour++) {
            const cell = document.createElement('div');
            cell.className = 'heatmap-cell';
            
            // Calculate performance for this hour/day
            let totalPnL = 0;
            let totalTrades = 0;
            let totalWins = 0;
            
            Object.keys(tradesByDate).forEach(dateStr => {
                const date = new Date(dateStr);
                if (date.getDay() === (day === 6 ? 0 : day + 1)) {
                    const dayTrades = tradesByDate[dateStr];
                    dayTrades.forEach(trade => {
                        if (trade.entry_time) {
                            const entryHour = new Date(trade.entry_time).getHours();
                            if (entryHour === hour) {
                                totalPnL += trade.profit_loss || 0;
                                totalTrades++;
                                if (trade.result === 'WIN') totalWins++;
                            }
                        }
                    });
                }
            });
            
            if (totalTrades > 0) {
                const avgPnL = totalPnL / totalTrades;
                const winRate = (totalWins / totalTrades) * 100;
                
                // Set color based on performance
                if (avgPnL > 100) {
                    cell.classList.add('very-positive');
                } else if (avgPnL > 50) {
                    cell.classList.add('positive');
                } else if (avgPnL > 0) {
                    cell.classList.add('slightly-positive');
                } else if (avgPnL < -100) {
                    cell.classList.add('very-negative');
                } else if (avgPnL < -50) {
                    cell.classList.add('negative');
                } else if (avgPnL < 0) {
                    cell.classList.add('slightly-negative');
                } else {
                    cell.classList.add('neutral');
                }
                
                // Add tooltip
                cell.addEventListener('mouseenter', (e) => {
                    showTooltip(e, `${days[day]} ${hour}h: Win Rate ${winRate.toFixed(0)}%, ${formatCurrency(avgPnL)} moyen`);
                });
                
                cell.addEventListener('mouseleave', () => {
                    hideTooltip();
                });
            } else {
                cell.classList.add('neutral');
            }
            
            grid.appendChild(cell);
        }
    }
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
 * Render best/worst days
 */
function renderBestWorstDays() {
    const bestDaysList = document.getElementById('bestDaysList');
    const worstDaysList = document.getElementById('worstDaysList');
    
    const dayStats = [];
    
    Object.keys(tradesByDate).forEach(dateStr => {
        const dayTrades = tradesByDate[dateStr];
        const dayPnL = dayTrades.reduce((sum, t) => sum + (t.profit_loss || 0), 0);
        dayStats.push({ date: dateStr, pnl: dayPnL });
    });
    
    // Sort by P&L
    dayStats.sort((a, b) => b.pnl - a.pnl);
    
    // Best days
    const bestDays = dayStats.slice(0, 3);
    bestDaysList.innerHTML = bestDays.map(day => `
        <div class="best-worst-item">
            <span class="best-worst-item-date">${formatDate(day.date)}</span>
            <span class="best-worst-item-value positive">${formatCurrency(day.pnl)}</span>
        </div>
    `).join('') || '<div class="best-worst-item"><span class="best-worst-item-date">Aucune donnée</span></div>';
    
    // Worst days
    const worstDays = dayStats.slice(-3).reverse();
    worstDaysList.innerHTML = worstDays.map(day => `
        <div class="best-worst-item">
            <span class="best-worst-item-date">${formatDate(day.date)}</span>
            <span class="best-worst-item-value negative">${formatCurrency(day.pnl)}</span>
        </div>
    `).join('') || '<div class="best-worst-item"><span class="best-worst-item-date">Aucune donnée</span></div>';
}

/**
 * Render monthly statistics
 */
function renderMonthlyStats() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    
    // Calculate weekly stats
    const weeklyStats = [];
    
    for (let week = 0; week < 5; week++) {
        const weekStart = new Date(year, month, week * 7 + 1);
        const weekEnd = new Date(weekStart);
        weekEnd.setDate(weekEnd.getDate() + 6);
        
        let weekPnL = 0;
        let weekTrades = 0;
        let weekWins = 0;
        let weekRR = 0;
        
        for (let d = new Date(weekStart); d <= weekEnd; d.setDate(d.getDate() + 1)) {
            const dateStr = d.toISOString().split('T')[0];
            const dayTrades = tradesByDate[dateStr] || [];
            
            weekTrades += dayTrades.length;
            weekPnL += dayTrades.reduce((sum, t) => sum + (t.profit_loss || 0), 0);
            weekWins += dayTrades.filter(t => t.result === 'WIN').length;
            weekRR += dayTrades.reduce((sum, t) => sum + (t.rr_obtained || 0), 0);
        }
        
        if (weekTrades > 0) {
            weeklyStats.push({
                week: week + 1,
                trades: weekTrades,
                pnl: weekPnL,
                winRate: (weekWins / weekTrades * 100).toFixed(1),
                avgRR: (weekRR / weekTrades).toFixed(2)
            });
        }
    }
    
    // Render weekly summary table
    const tbody = document.getElementById('weeklySummaryBody');
    tbody.innerHTML = weeklyStats.map(week => `
        <tr>
            <td>Semaine ${week.week}</td>
            <td>${week.trades}</td>
            <td class="${week.pnl >= 0 ? 'text-green' : 'text-red'}">${formatCurrency(week.pnl)}</td>
            <td>${week.winRate}%</td>
            <td>${week.avgRR}</td>
        </tr>
    `).join('') || '<tr><td colspan="5" class="empty-state">Aucune donnée</td></tr>';
    
    // Render charts
    renderPnLChart(weeklyStats);
    renderWinRateChart(weeklyStats);
}

/**
 * Render P&L chart
 */
function renderPnLChart(weeklyStats) {
    if (pnlChart) pnlChart.destroy();
    
    const categories = weeklyStats.map(w => `S${w.week}`);
    const series = weeklyStats.map(w => w.pnl);
    
    const options = {
        series: [{
            name: 'P&L',
            data: series
        }],
        chart: {
            type: 'bar',
            height: 250,
            fontFamily: 'Inter, sans-serif',
            background: 'transparent',
            toolbar: { show: false }
        },
        plotOptions: {
            bar: {
                borderRadius: 4,
                columnWidth: '60%'
            }
        },
        colors: series.map(v => v >= 0 ? '#00D26A' : '#FF4757'),
        xaxis: {
            categories: categories,
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
            y: { formatter: (value) => formatCurrency(value) }
        }
    };
    
    pnlChart = new ApexCharts(document.getElementById('pnlChart'), options);
    pnlChart.render();
}

/**
 * Render Win Rate chart
 */
function renderWinRateChart(weeklyStats) {
    if (winRateChart) winRateChart.destroy();
    
    const categories = weeklyStats.map(w => `S${w.week}`);
    const series = weeklyStats.map(w => parseFloat(w.winRate));
    
    const options = {
        series: [{
            name: 'Win Rate',
            data: series
        }],
        chart: {
            type: 'line',
            height: 250,
            fontFamily: 'Inter, sans-serif',
            background: 'transparent',
            toolbar: { show: false }
        },
        colors: ['#8B5CF6'],
        stroke: { curve: 'smooth', width: 2 },
        dataLabels: { enabled: false },
        xaxis: {
            categories: categories,
            labels: { style: { colors: '#8B9AB1', fontSize: '12px' } }
        },
        yaxis: {
            labels: {
                style: { colors: '#8B9AB1', fontSize: '12px' },
                formatter: (value) => `${value}%`
            },
            min: 0,
            max: 100
        },
        grid: { borderColor: '#1E2330', strokeDashArray: 4 },
        tooltip: {
            theme: 'dark',
            y: { formatter: (value) => `${value}%` }
        }
    };
    
    winRateChart = new ApexCharts(document.getElementById('winRateChart'), options);
    winRateChart.render();
}

/**
 * Show day details
 */
function showDayDetails(dateStr, dayTrades) {
    const panel = document.getElementById('dayDetailPanel');
    const title = document.getElementById('detailDateTitle');
    const subtitle = document.getElementById('detailDateSubtitle');
    const content = document.getElementById('detailContent');
    
    const date = new Date(dateStr);
    title.textContent = dayNames[date.getDay()];
    subtitle.textContent = formatDate(dateStr);
    
    // Calculate day stats
    const totalPnL = dayTrades.reduce((sum, t) => sum + (t.profit_loss || 0), 0);
    const wins = dayTrades.filter(t => t.result === 'WIN').length;
    const winRate = dayTrades.length > 0 ? (wins / dayTrades.length * 100).toFixed(1) : 0;
    const avgRR = dayTrades.reduce((sum, t) => sum + (t.rr_obtained || 0), 0) / dayTrades.length;
    
    // Load saved notes
    const savedNotes = localStorage.getItem(`day_notes_${dateStr}`) || '';
    
    content.innerHTML = `
        <div class="day-detail-section">
            <h3>Statistiques du jour</h3>
            <div class="day-stats-grid">
                <div class="day-stat-item">
                    <div class="day-stat-item-label">P&L Total</div>
                    <div class="day-stat-item-value ${totalPnL >= 0 ? 'text-green' : 'text-red'}">${formatCurrency(totalPnL)}</div>
                </div>
                <div class="day-stat-item">
                    <div class="day-stat-item-label">Win Rate</div>
                    <div class="day-stat-item-value">${winRate}%</div>
                </div>
                <div class="day-stat-item">
                    <div class="day-stat-item-label">Trades</div>
                    <div class="day-stat-item-value">${dayTrades.length}</div>
                </div>
                <div class="day-stat-item">
                    <div class="day-stat-item-label">RR Moyen</div>
                    <div class="day-stat-item-value">${avgRR.toFixed(2)}</div>
                </div>
            </div>
        </div>
        
        <div class="day-detail-section">
            <h3>Trades du jour</h3>
            ${dayTrades.map(trade => `
                <div class="day-trade-card" onclick="window.location.href='journal.html'">
                    <div class="day-trade-card-header">
                        <span class="day-trade-card-asset">${trade.asset}</span>
                        <span class="day-trade-card-direction ${trade.direction.toLowerCase()}">${trade.direction}</span>
                    </div>
                    <div class="day-trade-card-details">
                        <div class="day-trade-card-detail">
                            <span class="day-trade-card-detail-label">Heure</span>
                            <span class="day-trade-card-detail-value">${trade.entry_time ? new Date(trade.entry_time).toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' }) : '--'}</span>
                        </div>
                        <div class="day-trade-card-detail">
                            <span class="day-trade-card-detail-label">RR</span>
                            <span class="day-trade-card-detail-value">${formatNumber(trade.rr_obtained)}</span>
                        </div>
                        <div class="day-trade-card-detail">
                            <span class="day-trade-card-detail-label">P&L</span>
                            <span class="day-trade-card-detail-value ${trade.profit_loss >= 0 ? 'text-green' : 'text-red'}">${formatCurrency(trade.profit_loss)}</span>
                        </div>
                    </div>
                </div>
            `).join('') || '<p class="empty-state">Aucun trade ce jour</p>'}
        </div>
        
        <div class="day-detail-section">
            <h3>Notes du jour</h3>
            <textarea class="day-notes" id="dayNotes" placeholder="Ajoutez vos notes personnelles sur cette journée...">${savedNotes}</textarea>
            <button class="analyze-day-btn" onclick="analyzeDay('${dateStr}')">
                <i data-lucide="brain"></i>
                Analyser cette journée avec l'IA
            </button>
        </div>
    `;
    
    // Save notes on change
    setTimeout(() => {
        const notesTextarea = document.getElementById('dayNotes');
        if (notesTextarea) {
            notesTextarea.addEventListener('input', debounce((e) => {
                localStorage.setItem(`day_notes_${dateStr}`, e.target.value);
            }, 500));
        }
    }, 100);
    
    panel.classList.add('active');
    lucide.createIcons();
}

/**
 * Analyze day with AI
 */
async function analyzeDay(dateStr) {
    showToast('Analyse en cours...', 'info');
    
    try {
        const api = new API();
        const accountId = getActiveAccountId();
        
        if (!accountId) {
            showToast('Veuillez sélectionner un compte', 'error');
            return;
        }
        
        const response = await api.getAIAnalysis(accountId, '30d');
        showToast('Analyse terminée', 'success');
        
        // Could display the analysis in the panel
        
    } catch (error) {
        console.error('Error analyzing day:', error);
        showToast('Erreur lors de l\'analyse', 'error');
    }
}

/**
 * Handle account change
 */
function onAccountChange(accountId) {
    loadTrades().then(() => renderCurrentView());
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    initializeCommon();
    initializeCalendar();
});
