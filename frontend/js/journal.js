/**
 * Enhanced Journal functionality for SmartReview
 * Handles trade listing, filtering, CRUD operations, real-time calculations
 */

let allTrades = [];
let filteredTrades = [];
let currentPage = 1;
const tradesPerPage = 20;
let editingTradeId = null;
let currentQuickFilter = 'all';

/**
 * Load trades with pagination
 */
async function loadTrades() {
    showLoadingSkeleton();
    
    try {
        const accountId = getActiveAccountId();
        
        if (!accountId) {
            showEmptyTrades();
            return;
        }

        allTrades = await API.getTrades(accountId);
        applyFilters();
        renderTrades();
        updatePagination();
        updateTradesCounter();
        
    } catch (error) {
        console.error('Error loading trades:', error);
        showEmptyTrades();
        showToast('Erreur de chargement des trades', 'error');
    }
}

/**
 * Show loading skeleton
 */
function showLoadingSkeleton() {
    const tbody = document.getElementById('tradesTableBody');
    tbody.innerHTML = Array(5).fill('<tr><td colspan="12"><div class="skeleton skeleton-row"></div></td></tr>').join('');
}

/**
 * Render trades table with pagination
 */
function renderTrades() {
    const tbody = document.getElementById('tradesTableBody');
    
    if (!filteredTrades || filteredTrades.length === 0) {
        tbody.innerHTML = '<tr><td colspan="12" class="empty-state">Aucun trade trouvé</td></tr>';
        return;
    }

    // Calculate pagination
    const startIndex = (currentPage - 1) * tradesPerPage;
    const endIndex = startIndex + tradesPerPage;
    const pageTrades = filteredTrades.slice(startIndex, endIndex);

    tbody.innerHTML = pageTrades.map((trade, index) => `
        <tr onclick="viewTradeDetails(${trade.id})">
            <td>${startIndex + index + 1}</td>
            <td>
                <i data-lucide="dollar-sign" class="asset-icon"></i>
                <strong>${trade.asset}</strong>
            </td>
            <td><span class="direction-badge ${trade.direction.toLowerCase()}">${trade.direction}</span></td>
            <td>${formatDateTime(trade.trade_date)}</td>
            <td>${trade.setup || '--'}</td>
            <td><span class="session-badge">${trade.session || '--'}</span></td>
            <td>
                <div class="price-info">
                    E: ${formatNumber(trade.entry_price, 5)}<br>
                    SL: ${formatNumber(trade.stop_loss, 5)}<br>
                    TP: ${formatNumber(trade.take_profit, 5)}
                </div>
            </td>
            <td>
                <div class="price-info">
                    Prévu: ${formatNumber(trade.rr_planned)}<br>
                    Obtenu: ${formatNumber(trade.rr_obtained)}
                </div>
            </td>
            <td class="${getValueColor(trade.profit_loss)}">${formatCurrency(trade.profit_loss)}</td>
            <td><span class="score-badge ${getScoreClass(trade.trading_score)}">${trade.trading_score}</span></td>
            <td><span class="result-badge ${getResultClass(trade.result)}">${trade.result || 'En cours'}</span></td>
            <td>
                <div class="action-buttons">
                    <button class="action-btn" onclick="event.stopPropagation(); viewTradeDetails(${trade.id})">
                        <i data-lucide="eye"></i>
                    </button>
                    <button class="action-btn" onclick="event.stopPropagation(); editTrade(${trade.id})">
                        <i data-lucide="edit"></i>
                    </button>
                    <button class="action-btn" onclick="event.stopPropagation(); confirmDelete(${trade.id})">
                        <i data-lucide="trash-2"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
    
    lucide.createIcons();
}

/**
 * Get score class based on value
 */
function getScoreClass(score) {
    if (score >= 80) return 'high';
    if (score >= 60) return 'medium';
    return 'low';
}

/**
 * Get result class
 */
function getResultClass(result) {
    if (!result) return '';
    return result.toLowerCase();
}

/**
 * Apply filters including quick filters
 */
function applyFilters() {
    filteredTrades = allTrades.filter(trade => {
        // Quick filter
        if (currentQuickFilter === 'WIN' && trade.result !== 'WIN') return false;
        if (currentQuickFilter === 'LOSS' && trade.result !== 'LOSS') return false;
        if (currentQuickFilter === 'today') {
            const today = new Date().toDateString();
            if (new Date(trade.trade_date).toDateString() !== today) return false;
        }
        if (currentQuickFilter === 'week') {
            const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
            if (new Date(trade.trade_date) < weekAgo) return false;
        }
        
        return true;
    });
    
    currentPage = 1;
}

/**
 * Update pagination controls
 */
function updatePagination() {
    const totalPages = Math.ceil(filteredTrades.length / tradesPerPage) || 1;
    const prevBtn = document.getElementById('prevPage');
    const nextBtn = document.getElementById('nextPage');
    const pageInfo = document.getElementById('paginationInfo');
    
    pageInfo.textContent = `Page ${currentPage} sur ${totalPages}`;
    prevBtn.disabled = currentPage === 1;
    nextBtn.disabled = currentPage === totalPages;
}

/**
 * Update trades counter
 */
function updateTradesCounter() {
    const counter = document.getElementById('tradesCounter');
    counter.textContent = `${filteredTrades.length} trades affichés`;
}

/**
 * Show empty state
 */
function showEmptyTrades() {
    document.getElementById('tradesTableBody').innerHTML = 
        '<tr><td colspan="12" class="empty-state">Aucun trade enregistré</td></tr>';
    document.getElementById('tradesCounter').textContent = '0 trades affichés';
}

/**
 * View trade details in slide panel
 */
async function viewTradeDetails(tradeId) {
    try {
        const trade = await API.getTrade(tradeId);
        renderTradeDetailPanel(trade);
        document.getElementById('tradeDetailPanel').classList.add('active');
    } catch (error) {
        console.error('Error loading trade details:', error);
        showToast('Erreur lors du chargement des détails', 'error');
    }
}

/**
 * Render trade detail panel
 */
function renderTradeDetailPanel(trade) {
    const header = document.getElementById('detailHeader');
    const content = document.getElementById('detailContent');
    
    header.innerHTML = `
        <h2>${trade.asset} ${trade.direction}</h2>
        <span class="result-badge ${getResultClass(trade.result)}">${trade.result || 'En cours'}</span>
    `;
    
    content.innerHTML = `
        <div class="slide-panel-section">
            <h3>Informations Techniques</h3>
            <div class="detail-grid">
                <div class="detail-item">
                    <span class="detail-label">Date & Heure</span>
                    <span class="detail-value">${formatDateTime(trade.trade_date)}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Session</span>
                    <span class="detail-value">${trade.session || '--'}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Prix d'entrée</span>
                    <span class="detail-value">${formatNumber(trade.entry_price, 5)}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Stop Loss</span>
                    <span class="detail-value">${formatNumber(trade.stop_loss, 5)}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Take Profit</span>
                    <span class="detail-value">${formatNumber(trade.take_profit, 5)}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Prix de sortie</span>
                    <span class="detail-value">${formatNumber(trade.exit_price, 5)}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Taille position</span>
                    <span class="detail-value">${trade.lot_size} lots</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Risque engagé</span>
                    <span class="detail-value">${formatCurrency(trade.risk_amount)}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">RR Prévu</span>
                    <span class="detail-value">${formatNumber(trade.rr_planned)}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">RR Obtenu</span>
                    <span class="detail-value">${formatNumber(trade.rr_obtained)}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">P&L</span>
                    <span class="detail-value ${getValueColor(trade.profit_loss)}">${formatCurrency(trade.profit_loss)}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Setup</span>
                    <span class="detail-value">${trade.setup || '--'}</span>
                </div>
            </div>
        </div>
        
        <div class="slide-panel-section">
            <h3>Analyse Stratégique</h3>
            <div class="detail-grid">
                <div class="detail-item">
                    <span class="detail-label">Structure du marché</span>
                    <span class="detail-value">${trade.market_structure || '--'}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Liquidité ciblée</span>
                    <span class="detail-value">${trade.liquidity_targeted || '--'}</span>
                </div>
            </div>
            <div class="detail-item" style="margin-top: var(--spacing-md);">
                <span class="detail-label">Contexte de marché</span>
                <span class="detail-value">${trade.market_context || '--'}</span>
            </div>
            <div class="detail-item" style="margin-top: var(--spacing-md);">
                <span class="detail-label">Raisonnement</span>
                <span class="detail-value">${trade.reasoning || '--'}</span>
            </div>
        </div>
        
        <div class="slide-panel-section">
            <h3>Psychologie & Discipline</h3>
            <div class="detail-grid">
                <div class="detail-item">
                    <span class="detail-label">Confiance</span>
                    <span class="detail-value">${trade.confidence_level || '--'}/10</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">État émotionnel</span>
                    <span class="detail-value">${trade.emotional_state || '--'}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Discipline ressentie</span>
                    <span class="detail-value">${trade.discipline_felt || '--'}</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Plan respecté</span>
                    <span class="detail-value">${trade.plan_respected ? 'OUI' : 'NON'}</span>
                </div>
            </div>
        </div>
        
        <div class="slide-panel-section">
            <h3>Trading Score™️</h3>
            <div class="score-breakdown">
                <div class="score-item">
                    <span class="score-item-label">Plan respecté</span>
                    <span class="score-item-value">${trade.plan_respected ? '30' : '0'} pts</span>
                </div>
                <div class="score-item">
                    <span class="score-item-label">Confiance</span>
                    <span class="score-item-value">${(trade.confidence_level / 10 * 20).toFixed(0)} pts</span>
                </div>
                <div class="score-item">
                    <span class="score-item-label">Discipline</span>
                    <span class="score-item-value">${(trade.discipline_felt === 'excellent' ? 20 : trade.discipline_felt === 'good' ? 15 : 10)} pts</span>
                </div>
                <div class="score-item">
                    <span class="score-item-label">RR obtenu vs prévu</span>
                    <span class="score-item-value">${trade.rr_planned && trade.rr_obtained ? Math.min(30, (trade.rr_obtained / trade.rr_planned * 30).toFixed(0)) : '0'} pts</span>
                </div>
            </div>
            <div style="margin-top: var(--spacing-md); text-align: center;">
                <span class="modal-score-value ${getScoreClass(trade.trading_score)}">${trade.trading_score}</span>
                <span class="detail-label">/100</span>
            </div>
        </div>
        
        <div class="slide-panel-section">
            <h3>Screenshots</h3>
            <div class="screenshots-grid">
                <div class="screenshot-container">
                    ${trade.screenshot_before ? `<img src="${trade.screenshot_before}" alt="Avant">` : '<div style="padding: var(--spacing-xl); text-align: center; color: var(--text-muted);">Aucun screenshot</div>'}
                    <div class="screenshot-label">AVANT</div>
                </div>
                <div class="screenshot-container">
                    ${trade.screenshot_after ? `<img src="${trade.screenshot_after}" alt="Après">` : '<div style="padding: var(--spacing-xl); text-align: center; color: var(--text-muted);">Aucun screenshot</div>'}
                    <div class="screenshot-label">APRÈS</div>
                </div>
            </div>
        </div>
        
        <div class="slide-panel-section">
            <h3>Notes</h3>
            <div class="detail-item">
                <span class="detail-value">${trade.notes || 'Aucune note'}</span>
            </div>
        </div>
        
        <div class="panel-actions">
            <button class="btn btn-secondary" onclick="editTrade(${trade.id})">
                <i data-lucide="edit"></i>
                Éditer
            </button>
            <button class="btn btn-secondary" onclick="duplicateTrade(${trade.id})">
                <i data-lucide="copy"></i>
                Dupliquer
            </button>
            <button class="btn btn-danger" onclick="confirmDelete(${trade.id})">
                <i data-lucide="trash-2"></i>
                Supprimer
            </button>
        </div>
    `;
    
    lucide.createIcons();
}

/**
 * Edit trade
 */
async function editTrade(tradeId) {
    editingTradeId = tradeId;
    
    try {
        const trade = await API.getTrade(tradeId);
        
        // Populate form
        const form = document.getElementById('tradeForm');
        document.getElementById('modalTitle').textContent = 'Modifier Trade';
        
        // Set all form fields
        form.querySelector('[name="account_id"]').value = trade.account_id;
        form.querySelector('[name="asset"]').value = trade.asset;
        setDirectionToggle(trade.direction);
        setSessionToggle(trade.session);
        form.querySelector('[name="entry_price"]').value = trade.entry_price;
        form.querySelector('[name="stop_loss"]').value = trade.stop_loss || '';
        form.querySelector('[name="take_profit"]').value = trade.take_profit || '';
        form.querySelector('[name="exit_price"]').value = trade.exit_price || '';
        form.querySelector('[name="lot_size"]').value = trade.lot_size;
        form.querySelector('[name="risk_amount"]').value = trade.risk_amount || '';
        form.querySelector('[name="rr_planned"]').value = trade.rr_planned || '';
        form.querySelector('[name="rr_obtained"]').value = trade.rr_obtained || '';
        form.querySelector('[name="result"]').value = trade.result || '';
        form.querySelector('[name="profit_loss"]').value = trade.profit_loss || '';
        form.querySelector('[name="setup"]').value = trade.setup || '';
        form.querySelector('[name="market_structure"]').value = trade.market_structure || '';
        form.querySelector('[name="market_context"]').value = trade.market_context || '';
        form.querySelector('[name="liquidity_targeted"]').value = trade.liquidity_targeted || '';
        form.querySelector('[name="reasoning"]').value = trade.reasoning || '';
        form.querySelector('[name="confidence_level"]').value = trade.confidence_level || 5;
        document.getElementById('confidenceValue').textContent = trade.confidence_level || 5;
        setEmotionToggle(trade.emotional_state);
        form.querySelector('[name="discipline_felt"]').value = trade.discipline_felt || 5;
        document.getElementById('disciplineValue').textContent = trade.discipline_felt || 5;
        setPlanToggle(trade.plan_respected);
        form.querySelector('[name="notes"]').value = trade.notes || '';
        
        // Calculate and update score
        calculateTradingScore();
        
        // Open modal
        document.getElementById('tradeModal').classList.add('active');
        document.getElementById('tradeDetailPanel').classList.remove('active');
        
    } catch (error) {
        console.error('Error loading trade for edit:', error);
        showToast('Erreur lors du chargement du trade', 'error');
    }
}

/**
 * Duplicate trade
 */
async function duplicateTrade(tradeId) {
    editingTradeId = null;
    
    try {
        const trade = await API.getTrade(tradeId);
        
        // Populate form with trade data but clear result/exit
        const form = document.getElementById('tradeForm');
        document.getElementById('modalTitle').textContent = 'Dupliquer Trade';
        
        form.querySelector('[name="account_id"]').value = trade.account_id;
        form.querySelector('[name="asset"]').value = trade.asset;
        setDirectionToggle(trade.direction);
        setSessionToggle(trade.session);
        form.querySelector('[name="entry_price"]').value = trade.entry_price;
        form.querySelector('[name="stop_loss"]').value = trade.stop_loss || '';
        form.querySelector('[name="take_profit"]').value = trade.take_profit || '';
        form.querySelector('[name="exit_price"]').value = '';
        form.querySelector('[name="lot_size"]').value = trade.lot_size;
        form.querySelector('[name="risk_amount"]').value = trade.risk_amount || '';
        form.querySelector('[name="rr_planned"]').value = '';
        form.querySelector('[name="rr_obtained"]').value = '';
        form.querySelector('[name="result"]').value = '';
        form.querySelector('[name="profit_loss"]').value = '';
        form.querySelector('[name="setup"]').value = trade.setup || '';
        form.querySelector('[name="market_structure"]').value = trade.market_structure || '';
        form.querySelector('[name="market_context"]').value = trade.market_context || '';
        form.querySelector('[name="liquidity_targeted"]').value = trade.liquidity_targeted || '';
        form.querySelector('[name="reasoning"]').value = trade.reasoning || '';
        form.querySelector('[name="confidence_level"]').value = trade.confidence_level || 5;
        document.getElementById('confidenceValue').textContent = trade.confidence_level || 5;
        setEmotionToggle(trade.emotional_state);
        form.querySelector('[name="discipline_felt"]').value = trade.discipline_felt || 5;
        document.getElementById('disciplineValue').textContent = trade.discipline_felt || 5;
        setPlanToggle(trade.plan_respected);
        form.querySelector('[name="notes"]').value = trade.notes || '';
        
        calculateTradingScore();
        
        document.getElementById('tradeModal').classList.add('active');
        document.getElementById('tradeDetailPanel').classList.remove('active');
        
    } catch (error) {
        console.error('Error duplicating trade:', error);
        showToast('Erreur lors de la duplication', 'error');
    }
}

/**
 * Set direction toggle
 */
function setDirectionToggle(direction) {
    const buttons = document.querySelectorAll('.toggle-btn[data-value="BUY"], .toggle-btn[data-value="SELL"]');
    buttons.forEach(btn => {
        btn.classList.remove('active', 'buy', 'sell');
        if (btn.dataset.value === direction) {
            btn.classList.add('active', direction.toLowerCase());
        }
    });
    document.getElementById('directionInput').value = direction;
}

/**
 * Set session toggle
 */
function setSessionToggle(session) {
    const buttons = document.querySelectorAll('.toggle-btn[data-value="ASIA"], .toggle-btn[data-value="LONDON"], .toggle-btn[data-value="NEW_YORK"]');
    buttons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.value === session) {
            btn.classList.add('active');
        }
    });
    document.getElementById('sessionInput').value = session || '';
}

/**
 * Set emotion toggle
 */
function setEmotionToggle(emotion) {
    const buttons = document.querySelectorAll('.emotion-btn');
    buttons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.value === emotion) {
            btn.classList.add('active');
        }
    });
    document.getElementById('emotionalStateInput').value = emotion || '';
}

/**
 * Set plan toggle
 */
function setPlanToggle(respected) {
    const buttons = document.querySelectorAll('.plan-btn');
    buttons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.value === String(respected)) {
            btn.classList.add('active');
        }
    });
    document.getElementById('planRespectedInput').value = respected;
}

/**
 * Confirm delete
 */
function confirmDelete(tradeId) {
    window.pendingDeleteId = tradeId;
    document.getElementById('deleteModal').classList.add('active');
    document.getElementById('tradeDetailPanel').classList.remove('active');
}

/**
 * Delete trade
 */
async function deleteTrade(tradeId) {
    try {
        await API.deleteTrade(tradeId);
        showToast('Trade supprimé avec succès', 'success');
        document.getElementById('deleteModal').classList.remove('active');
        loadTrades();
    } catch (error) {
        console.error('Error deleting trade:', error);
        showToast('Erreur lors de la suppression du trade', 'error');
    }
}

/**
 * Real-time calculations
 */
function calculateRR() {
    const entry = parseFloat(document.getElementById('entryPrice').value);
    const sl = parseFloat(document.getElementById('stopLoss').value);
    const tp = parseFloat(document.getElementById('takeProfit').value);
    const exit = parseFloat(document.getElementById('exitPrice').value);
    const direction = document.getElementById('directionInput').value;
    
    let rrPlanned = 0;
    let rrObtained = 0;
    
    if (entry && sl && tp) {
        if (direction === 'BUY') {
            rrPlanned = (tp - entry) / (entry - sl);
        } else {
            rrPlanned = (entry - tp) / (sl - entry);
        }
    }
    
    if (entry && sl && exit) {
        if (direction === 'BUY') {
            rrObtained = (exit - entry) / (entry - sl);
        } else {
            rrObtained = (entry - exit) / (sl - entry);
        }
    }
    
    document.getElementById('rrPlanned').value = rrPlanned > 0 ? rrPlanned.toFixed(2) : '';
    document.getElementById('rrObtained').value = rrObtained > 0 ? rrObtained.toFixed(2) : '';
    
    calculatePnL();
}

/**
 * Calculate P&L
 */
function calculatePnL() {
    const entry = parseFloat(document.getElementById('entryPrice').value);
    const exit = parseFloat(document.getElementById('exitPrice').value);
    const lots = parseFloat(document.getElementById('lotSize').value);
    const risk = parseFloat(document.getElementById('riskAmount').value);
    const rrObtained = parseFloat(document.getElementById('rrObtained').value);
    
    let pnl = 0;
    
    if (risk && rrObtained) {
        // Simplified: P&L = Risk × RR Obtained
        pnl = risk * rrObtained;
    }
    
    document.getElementById('profitLoss').value = pnl !== 0 ? pnl.toFixed(2) : '';
    
    // Auto-detect result
    const resultSelect = document.getElementById('resultSelect');
    if (pnl > 0) {
        resultSelect.value = 'WIN';
    } else if (pnl < 0) {
        resultSelect.value = 'LOSS';
    } else if (pnl === 0 && exit) {
        resultSelect.value = 'BREAKEVEN';
    }
    
    calculateTradingScore();
}

/**
 * Calculate Trading Score
 */
function calculateTradingScore() {
    const planRespected = document.getElementById('planRespectedInput').value === 'true';
    const confidence = parseInt(document.querySelector('[name="confidence_level"]').value) || 5;
    const discipline = parseInt(document.querySelector('[name="discipline_felt"]').value) || 5;
    const rrPlanned = parseFloat(document.getElementById('rrPlanned').value) || 0;
    const rrObtained = parseFloat(document.getElementById('rrObtained').value) || 0;
    
    let score = 0;
    
    // Plan respected: 30 pts
    if (planRespected) score += 30;
    
    // Confidence: 0-20 pts
    score += (confidence / 10) * 20;
    
    // Discipline: 0-20 pts
    score += (discipline / 10) * 20;
    
    // RR ratio: 0-30 pts
    if (rrPlanned > 0 && rrObtained > 0) {
        const rrRatio = rrObtained / rrPlanned;
        score += Math.min(30, rrRatio * 30);
    }
    
    score = Math.min(100, Math.round(score));
    
    // Update display
    const scoreValue = document.getElementById('modalScoreValue');
    scoreValue.textContent = score;
    scoreValue.className = 'modal-score-value ' + getScoreClass(score);
    
    // Update breakdown
    const breakdown = document.getElementById('modalScoreBreakdown');
    breakdown.textContent = `Plan: ${planRespected ? 30 : 0} | Confiance: ${Math.round((confidence / 10) * 20)} | Discipline: ${Math.round((discipline / 10) * 20)} | RR: ${Math.min(30, rrPlanned > 0 && rrObtained > 0 ? Math.round((rrObtained / rrPlanned) * 30) : 0)}`;
}

/**
 * Handle account change
 */
function onAccountChange(accountId) {
    loadTrades();
}

/**
 * Initialize journal
 */
function initializeJournal() {
    // Quick filters
    document.querySelectorAll('.quick-filter-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.quick-filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentQuickFilter = btn.dataset.filter;
            applyFilters();
            renderTrades();
            updatePagination();
            updateTradesCounter();
        });
    });

    // Search functionality
    const searchInput = document.getElementById('searchTrades');
    if (searchInput) {
        searchInput.addEventListener('input', debounce((e) => {
            const query = e.target.value.toLowerCase();
            if (query === '') {
                applyFilters();
            } else {
                filteredTrades = allTrades.filter(trade => 
                    trade.asset.toLowerCase().includes(query) ||
                    (trade.setup && trade.setup.toLowerCase().includes(query)) ||
                    (trade.reasoning && trade.reasoning.toLowerCase().includes(query))
                );
            }
            currentPage = 1;
            renderTrades();
            updatePagination();
            updateTradesCounter();
        }, 300));
    }

    // Pagination
    document.getElementById('prevPage').addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            renderTrades();
            updatePagination();
        }
    });

    document.getElementById('nextPage').addEventListener('click', () => {
        const totalPages = Math.ceil(filteredTrades.length / tradesPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            renderTrades();
            updatePagination();
        }
    });

    // Tab navigation
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
        });
    });

    // Direction toggle
    document.querySelectorAll('.toggle-btn[data-value="BUY"], .toggle-btn[data-value="SELL"]').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.toggle-btn[data-value="BUY"], .toggle-btn[data-value="SELL"]').forEach(b => {
                b.classList.remove('active', 'buy', 'sell');
            });
            btn.classList.add('active', btn.dataset.value.toLowerCase());
            document.getElementById('directionInput').value = btn.dataset.value;
            calculateRR();
        });
    });

    // Session toggle
    document.querySelectorAll('.toggle-btn[data-value="ASIA"], .toggle-btn[data-value="LONDON"], .toggle-btn[data-value="NEW_YORK"]').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.toggle-btn[data-value="ASIA"], .toggle-btn[data-value="LONDON"], .toggle-btn[data-value="NEW_YORK"]').forEach(b => {
                b.classList.remove('active');
            });
            btn.classList.add('active');
            document.getElementById('sessionInput').value = btn.dataset.value;
        });
    });

    // Emotion toggle
    document.querySelectorAll('.emotion-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.emotion-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById('emotionalStateInput').value = btn.dataset.value;
        });
    });

    // Plan toggle
    document.querySelectorAll('.plan-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.plan-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById('planRespectedInput').value = btn.dataset.value;
            calculateTradingScore();
        });
    });

    // Sliders
    document.getElementById('confidenceSlider').addEventListener('input', (e) => {
        document.getElementById('confidenceValue').textContent = e.target.value;
        calculateTradingScore();
    });

    document.getElementById('disciplineSlider').addEventListener('input', (e) => {
        document.getElementById('disciplineValue').textContent = e.target.value;
        calculateTradingScore();
    });

    // Price inputs for RR calculation
    ['entryPrice', 'stopLoss', 'takeProfit', 'exitPrice'].forEach(id => {
        document.getElementById(id).addEventListener('input', calculateRR);
    });

    // Risk amount for P&L calculation
    document.getElementById('riskAmount').addEventListener('input', calculatePnL);

    // Upload zones
    setupUploadZone('uploadBefore', 'fileBefore', 'previewBefore');
    setupUploadZone('uploadAfter', 'fileAfter', 'previewAfter');

    // Logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', logout);
    }

    // New trade modal
    const modal = document.getElementById('tradeModal');
    const form = document.getElementById('tradeForm');
    
    document.getElementById('newTradeBtn').addEventListener('click', () => {
        editingTradeId = null;
        form.reset();
        document.getElementById('modalTitle').textContent = 'Nouveau Trade';
        
        // Reset toggles
        setDirectionToggle('BUY');
        document.querySelectorAll('.emotion-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.plan-btn').forEach(b => b.classList.remove('active'));
        document.querySelector('.plan-btn[data-value="true"]').classList.add('active');
        
        // Reset sliders
        document.getElementById('confidenceSlider').value = 5;
        document.getElementById('confidenceValue').textContent = '5';
        document.getElementById('disciplineSlider').value = 5;
        document.getElementById('disciplineValue').textContent = '5';
        
        // Reset score
        document.getElementById('modalScoreValue').textContent = '0';
        document.getElementById('modalScoreValue').className = 'modal-score-value';
        document.getElementById('modalScoreBreakdown').textContent = 'Plan: 0 | Confiance: 0 | Discipline: 0 | RR: 0';
        
        // Clear previews
        document.getElementById('previewBefore').innerHTML = '';
        document.getElementById('previewAfter').innerHTML = '';
        
        // Set today's date
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('entryDate').value = today;
        
        // Load accounts
        loadAccountsIntoForm();
        
        modal.classList.add('active');
    });
    
    document.getElementById('closeModal').addEventListener('click', () => {
        modal.classList.remove('active');
        editingTradeId = null;
    });
    
    document.getElementById('cancelModal').addEventListener('click', () => {
        modal.classList.remove('active');
        editingTradeId = null;
    });

    // Form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const saveBtn = document.getElementById('saveTradeBtn');
        saveBtn.disabled = true;
        saveBtn.innerHTML = '<i data-lucide="loader-2" class="spin"></i> Enregistrement...';
        
        const formData = new FormData(form);
        
        // Combine date and time
        const entryDate = formData.get('entry_date');
        const entryTime = formData.get('entry_time');
        const exitDate = formData.get('exit_date');
        const exitTime = formData.get('exit_time');
        
        const entryDateTime = entryDate && entryTime ? `${entryDate}T${entryTime}` : null;
        const exitDateTime = exitDate && exitTime ? `${exitDate}T${exitTime}` : null;

        const tradeData = {
            account_id: parseInt(formData.get('account_id')),
            asset: formData.get('asset'),
            direction: formData.get('direction'),
            entry_price: parseFloat(formData.get('entry_price')),
            stop_loss: formData.get('stop_loss') ? parseFloat(formData.get('stop_loss')) : null,
            take_profit: formData.get('take_profit') ? parseFloat(formData.get('take_profit')) : null,
            exit_price: formData.get('exit_price') ? parseFloat(formData.get('exit_price')) : null,
            lot_size: parseFloat(formData.get('lot_size')),
            risk_amount: formData.get('risk_amount') ? parseFloat(formData.get('risk_amount')) : null,
            rr_planned: formData.get('rr_planned') ? parseFloat(formData.get('rr_planned')) : null,
            rr_obtained: formData.get('rr_obtained') ? parseFloat(formData.get('rr_obtained')) : null,
            result: formData.get('result') || null,
            profit_loss: formData.get('profit_loss') ? parseFloat(formData.get('profit_loss')) : 0,
            setup: formData.get('setup'),
            market_structure: formData.get('market_structure'),
            market_context: formData.get('market_context'),
            liquidity_targeted: formData.get('liquidity_targeted'),
            reasoning: formData.get('reasoning'),
            confidence_level: parseInt(formData.get('confidence_level')),
            emotional_state: formData.get('emotional_state'),
            discipline_felt: parseInt(formData.get('discipline_felt')),
            plan_respected: formData.get('plan_respected') === 'true',
            session: formData.get('session'),
            entry_time: entryDateTime,
            exit_time: exitDateTime,
            notes: formData.get('notes')
        };

        try {
            const api = new API();
            
            if (editingTradeId) {
                await api.updateTrade(editingTradeId, tradeData);
                showToast('Trade modifié avec succès', 'success');
            } else {
                await api.createTrade(tradeData);
                showToast('Trade créé avec succès', 'success');
            }
            
            modal.classList.remove('active');
            editingTradeId = null;
            loadTrades();
            
        } catch (error) {
            console.error('Error saving trade:', error);
            showToast('Erreur lors de l\'enregistrement du trade', 'error');
        } finally {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '<i data-lucide="save"></i> Enregistrer';
            lucide.createIcons();
        }
    });

    // Detail panel close
    document.getElementById('closeDetailPanel').addEventListener('click', () => {
        document.getElementById('tradeDetailPanel').classList.remove('active');
    });

    // Delete modal
    document.getElementById('closeDeleteModal').addEventListener('click', () => {
        document.getElementById('deleteModal').classList.remove('active');
    });

    document.getElementById('cancelDelete').addEventListener('click', () => {
        document.getElementById('deleteModal').classList.remove('active');
    });

    document.getElementById('confirmDelete').addEventListener('click', () => {
        if (window.pendingDeleteId) {
            deleteTrade(window.pendingDeleteId);
            window.pendingDeleteId = null;
        }
    });

    // Initial load
    setTimeout(loadTrades, 500);
}

/**
 * Load accounts into form
 */
async function loadAccountsIntoForm() {
    try {
        const api = new API();
        const accounts = await api.getAccounts();
        const select = document.getElementById('formAccount');
        select.innerHTML = '<option value="">Sélectionner</option>' + 
            accounts.map(a => `<option value="${a.id}">${a.name}</option>`).join('');
        
        // Set active account
        const activeAccountId = getActiveAccountId();
        if (activeAccountId) {
            select.value = activeAccountId;
        }
    } catch (error) {
        console.error('Error loading accounts:', error);
    }
}

/**
 * Setup upload zone
 */
function setupUploadZone(zoneId, inputId, previewId) {
    const zone = document.getElementById(zoneId);
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    
    zone.addEventListener('click', () => input.click());
    
    zone.addEventListener('dragover', (e) => {
        e.preventDefault();
        zone.style.borderColor = 'var(--accent-blue)';
    });
    
    zone.addEventListener('dragleave', () => {
        zone.style.borderColor = 'var(--border)';
    });
    
    zone.addEventListener('drop', (e) => {
        e.preventDefault();
        zone.style.borderColor = 'var(--border)';
        
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleFileUpload(file, preview);
        }
    });
    
    input.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFileUpload(file, preview);
        }
    });
}

/**
 * Handle file upload
 */
function handleFileUpload(file, previewContainer) {
    const reader = new FileReader();
    reader.onload = (e) => {
        const img = document.createElement('img');
        img.src = e.target.result;
        previewContainer.innerHTML = '';
        previewContainer.appendChild(img);
    };
    reader.readAsDataURL(file);
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    initializeCommon();
    initializeJournal();
});
