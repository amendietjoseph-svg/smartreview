/**
 * Accounts Management for SmartReview
 * Handles multi-account management, prop firm dashboard, and account comparison
 */

let accounts = [];
let selectedAccount = null;
let comparisonChart = null;

/**
 * Initialize accounts page
 */
async function initializeAccounts() {
    await loadAccounts();
    setupEventListeners();
}

/**
 * Load accounts from backend
 */
async function loadAccounts() {
    try {
        const api = new API();
        accounts = await api.getAccounts();
        renderAccounts();
        updateAccountSelector();
        
        // Show comparison if multiple accounts
        if (accounts.length > 1) {
            document.getElementById('comparisonSection').style.display = 'block';
            renderComparisonChart();
            renderComparisonTable();
        }
        
    } catch (error) {
        console.error('Error loading accounts:', error);
        document.getElementById('accountsGrid').innerHTML = '<div class="empty-state">Erreur de chargement</div>';
    }
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // New account button
    document.getElementById('newAccountBtn').addEventListener('click', () => {
        openAccountModal();
    });

    // Modal handling
    document.getElementById('closeModal').addEventListener('click', closeAccountModal);
    document.getElementById('cancelModal').addEventListener('click', closeAccountModal);

    // Account type change
    document.getElementById('accountType').addEventListener('change', (e) => {
        toggleAccountTypeFields(e.target.value);
    });

    // Broker change
    const brokerSelect = document.querySelector('select[name="broker"]');
    if (brokerSelect) {
        brokerSelect.addEventListener('change', (e) => {
            const otherField = document.getElementById('otherBrokerField');
            if (e.target.value === 'Autre') {
                otherField.style.display = 'block';
            } else {
                otherField.style.display = 'none';
            }
        });
    }

    // Form submission
    document.getElementById('accountForm').addEventListener('submit', handleAccountSubmit);

    // Account selector change
    const accountSelector = document.getElementById('activeAccount');
    if (accountSelector) {
        accountSelector.addEventListener('change', (e) => {
            selectedAccount = accounts.find(a => a.id === parseInt(e.target.value));
            if (selectedAccount && selectedAccount.type === 'PROP_FIRM') {
                showPropFirmDashboard(selectedAccount);
            } else {
                document.getElementById('propFirmDashboard').style.display = 'none';
            }
        });
    }
}

/**
 * Render accounts grid
 */
function renderAccounts() {
    const grid = document.getElementById('accountsGrid');
    
    if (accounts.length === 0) {
        grid.innerHTML = '<div class="empty-state">Aucun compte. Créez votre premier compte !</div>';
        return;
    }
    
    grid.innerHTML = accounts.map(account => {
        const isActive = account.is_active;
        const typeBadge = account.type === 'PROP_FIRM' ? 'prop-firm' : 'personal';
        const typeLabel = account.type === 'PROP_FIRM' ? 'Prop Firm' : 'Personnel';
        
        // Calculate account stats
        const totalPnL = account.current_balance - account.initial_balance;
        const pnlClass = totalPnL >= 0 ? 'positive' : 'negative';
        
        return `
            <div class="account-card ${isActive ? '' : 'inactive'}" onclick="selectAccount(${account.id})">
                <div class="account-card-header">
                    <div class="account-info">
                        <h3>${account.name}</h3>
                        <span class="account-type-badge ${typeBadge}">${typeLabel}</span>
                    </div>
                    <div class="account-status">
                        <span class="status-dot ${isActive ? 'online' : 'offline'}"></span>
                    </div>
                </div>
                <div class="account-card-body">
                    <div class="account-metric">
                        <span class="metric-label">Broker/PropFirm</span>
                        <span class="metric-value">${account.broker || account.prop_firm_name || '--'}</span>
                    </div>
                    <div class="account-metric">
                        <span class="metric-label">Solde Actuel</span>
                        <span class="metric-value">$${account.current_balance?.toFixed(2) || '0.00'}</span>
                    </div>
                    <div class="account-metric">
                        <span class="metric-label">Variation</span>
                        <span class="metric-value ${pnlClass}">${totalPnL >= 0 ? '+' : ''}${formatCurrency(totalPnL)}</span>
                    </div>
                    ${account.type === 'PROP_FIRM' ? `
                    <div class="account-metric">
                        <span class="metric-label">Phase</span>
                        <span class="metric-value">${account.challenge_phase || '--'}</span>
                    </div>
                    ` : ''}
                </div>
                <div class="account-card-footer">
                    <button class="btn btn-sm btn-secondary" onclick="event.stopPropagation(); editAccount(${account.id})">
                        <i data-lucide="edit"></i>
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="event.stopPropagation(); deleteAccount(${account.id})">
                        <i data-lucide="trash-2"></i>
                    </button>
                </div>
            </div>
        `;
    }).join('');
    
    lucide.createIcons();
}

/**
 * Select account
 */
function selectAccount(accountId) {
    const account = accounts.find(a => a.id === accountId);
    if (account) {
        selectedAccount = account;
        document.getElementById('activeAccount').value = accountId;
        
        if (account.type === 'PROP_FIRM') {
            showPropFirmDashboard(account);
        } else {
            document.getElementById('propFirmDashboard').style.display = 'none';
        }
    }
}

/**
 * Show prop firm dashboard
 */
function showPropFirmDashboard(account) {
    const dashboard = document.getElementById('propFirmDashboard');
    dashboard.style.display = 'block';
    
    // Update header
    document.getElementById('propFirmName').textContent = `${account.prop_firm_name} Challenge`;
    document.getElementById('propFirmPhase').textContent = account.challenge_phase || 'Phase 1';
    
    // Calculate progress
    const initialBalance = account.initial_balance || 10000;
    const currentBalance = account.current_balance || initialBalance;
    const profitTarget = account.profit_target || 10;
    const currentProfit = ((currentBalance - initialBalance) / initialBalance * 100);
    const profitProgress = Math.min((currentProfit / profitTarget * 100), 100);
    
    // Update profit progress
    const profitProgressBar = document.getElementById('profitProgressBar');
    profitProgressBar.style.width = `${profitProgress}%`;
    profitProgressBar.textContent = `${currentProfit.toFixed(1)}% / ${profitTarget}%`;
    profitProgressBar.className = 'progress-fill ' + (profitProgress >= 80 ? 'green' : profitProgress >= 50 ? 'orange' : 'red');
    
    document.getElementById('profitProgress').textContent = `${currentProfit.toFixed(1)}% / ${profitTarget}%`;
    
    // Calculate days progress (simplified)
    const minDays = account.min_days || 30;
    const daysTraded = Math.floor(Math.random() * minDays) + 5; // Placeholder
    const daysProgress = Math.min((daysTraded / minDays * 100), 100);
    
    const daysProgressBar = document.getElementById('daysProgressBar');
    daysProgressBar.style.width = `${daysProgress}%`;
    daysProgressBar.textContent = `${daysProgress.toFixed(0)}%`;
    daysProgressBar.className = 'progress-fill ' + (daysProgress >= 50 ? 'green' : 'orange');
    
    document.getElementById('daysProgress').textContent = `${daysTraded} / ${minDays} jours`;
    
    // Calculate drawdown
    const dailyDDLimit = account.daily_drawdown_limit || 5;
    const maxDDLimit = account.max_drawdown_limit || 10;
    const currentDailyDD = Math.random() * dailyDDLimit; // Placeholder
    const currentMaxDD = Math.random() * maxDDLimit; // Placeholder
    
    const dailyDDPercent = (currentDailyDD / dailyDDLimit * 100);
    const maxDDPercent = (currentMaxDD / maxDDLimit * 100);
    
    const dailyDDGauge = document.getElementById('dailyDDGauge');
    dailyDDGauge.textContent = `${currentDailyDD.toFixed(1)}%`;
    dailyDDGauge.className = 'gauge-value ' + (dailyDDPercent < 50 ? 'green' : dailyDDPercent < 80 ? 'orange' : 'red');
    
    const maxDDGauge = document.getElementById('maxDDGauge');
    maxDDGauge.textContent = `${currentMaxDD.toFixed(1)}%`;
    maxDDGauge.className = 'gauge-value ' + (maxDDPercent < 50 ? 'green' : maxDDPercent < 80 ? 'orange' : 'red');
    
    // Calculate recommendations
    const dailyDDRemaining = dailyDDLimit - currentDailyDD;
    const maxDDRemaining = maxDDLimit - currentMaxDD;
    const optimalRisk = Math.min(dailyDDRemaining * 0.3, maxDDRemaining * 0.1);
    
    // Update recommendations
    const recommendationsCard = document.querySelector('.recommendations-card');
    recommendationsCard.innerHTML = `
        <h3>Recommandations Dynamiques</h3>
        <div class="recommendation-item">
            <span class="recommendation-icon">💡</span>
            <div>
                <strong>Risque optimal recommandé</strong>
                <p>${optimalRisk.toFixed(2)}% du capital pour les prochains trades</p>
            </div>
        </div>
        <div class="recommendation-item">
            <span class="recommendation-icon">📊</span>
            <div>
                <strong>Trades restants conseillés</strong>
                <p>${Math.max(0, 3 - Math.floor(Math.random() * 3))} trades maximum aujourd'hui</p>
            </div>
        </div>
        ${dailyDDPercent > 70 ? `
        <div class="recommendation-item" style="background: rgba(255, 71, 87, 0.1);">
            <span class="recommendation-icon">⚠️</span>
            <div>
                <strong>Attention</strong>
                <p>Drawdown journalier à ${dailyDDPercent.toFixed(0)}% de la limite</p>
            </div>
        </div>
        ` : ''}
    `;
    
    // Render history (placeholder)
    document.getElementById('propFirmHistory').innerHTML = `
        <div class="recommendation-item">
            <span class="recommendation-icon">✅</span>
            <div>
                <strong>FTMO Challenge Phase 1</strong>
                <p>RÉUSSI - 12% profit en 18 jours</p>
            </div>
        </div>
        <div class="recommendation-item">
            <span class="recommendation-icon">❌</span>
            <div>
                <strong>FTMO Challenge Phase 2</strong>
                <p>ÉCHOUÉ - Drawdown max dépassé</p>
            </div>
        </div>
    `;
}

/**
 * Toggle account type fields
 */
function toggleAccountTypeFields(type) {
    const personalFields = document.querySelectorAll('.personal-field');
    const propFirmFields = document.querySelectorAll('.prop-firm-field');
    
    if (type === 'PERSONAL') {
        personalFields.forEach(field => field.style.display = 'block');
        propFirmFields.forEach(field => field.style.display = 'none');
    } else {
        personalFields.forEach(field => field.style.display = 'none');
        propFirmFields.forEach(field => field.style.display = 'block');
    }
}

/**
 * Open account modal
 */
function openAccountModal(account = null) {
    const modal = document.getElementById('accountModal');
    const form = document.getElementById('accountForm');
    const title = document.getElementById('modalTitle');
    
    form.reset();
    
    if (account) {
        title.textContent = 'Éditer Compte';
        form.dataset.editId = account.id;
        
        // Populate form
        form.querySelector('[name="name"]').value = account.name;
        form.querySelector('[name="type"]').value = account.type;
        form.querySelector('[name="currency"]').value = account.currency || 'USD';
        form.querySelector('[name="broker"]').value = account.broker || '';
        form.querySelector('[name="prop_firm_name"]').value = account.prop_firm_name || '';
        form.querySelector('[name="challenge_phase"]').value = account.challenge_phase || '';
        form.querySelector('[name="initial_balance"]').value = account.initial_balance;
        form.querySelector('[name="current_balance"]').value = account.current_balance;
        form.querySelector('[name="profit_target"]').value = account.profit_target || '';
        form.querySelector('[name="daily_drawdown_limit"]').value = account.daily_drawdown_limit || '';
        form.querySelector('[name="max_drawdown_limit"]').value = account.max_drawdown_limit || '';
        form.querySelector('[name="min_days"]').value = account.min_days || '';
        
        toggleAccountTypeFields(account.type);
    } else {
        title.textContent = 'Nouveau Compte';
        delete form.dataset.editId;
        toggleAccountTypeFields('PERSONAL');
    }
    
    modal.classList.add('active');
}

/**
 * Close account modal
 */
function closeAccountModal() {
    document.getElementById('accountModal').classList.remove('active');
}

/**
 * Handle account form submission
 */
async function handleAccountSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const editId = form.dataset.editId;
    
    const broker = formData.get('broker');
    const brokerOther = formData.get('broker_other');
    const finalBroker = broker === 'Autre' ? brokerOther : broker;
    
    const accountData = {
        name: formData.get('name'),
        type: formData.get('type'),
        currency: formData.get('currency'),
        broker: finalBroker,
        prop_firm_name: formData.get('prop_firm_name'),
        challenge_phase: formData.get('challenge_phase'),
        initial_balance: parseFloat(formData.get('initial_balance')),
        current_balance: parseFloat(formData.get('current_balance')),
        profit_target: formData.get('profit_target') ? parseFloat(formData.get('profit_target')) : null,
        daily_drawdown_limit: formData.get('daily_drawdown_limit') ? parseFloat(formData.get('daily_drawdown_limit')) : null,
        max_drawdown_limit: formData.get('max_drawdown_limit') ? parseFloat(formData.get('max_drawdown_limit')) : null,
        min_days: formData.get('min_days') ? parseInt(formData.get('min_days')) : null,
        created_at: formData.get('created_at') || new Date().toISOString().split('T')[0],
        is_active: true
    };
    
    try {
        const api = new API();
        
        if (editId) {
            await api.updateAccount(parseInt(editId), accountData);
            showToast('Compte mis à jour avec succès', 'success');
        } else {
            await api.createAccount(accountData);
            showToast('Compte créé avec succès', 'success');
        }
        
        closeAccountModal();
        loadAccounts();
        
    } catch (error) {
        console.error('Error saving account:', error);
        showToast('Erreur lors de la sauvegarde du compte', 'error');
    }
}

/**
 * Edit account
 */
function editAccount(accountId) {
    const account = accounts.find(a => a.id === accountId);
    if (account) {
        openAccountModal(account);
    }
}

/**
 * Delete account
 */
async function deleteAccount(accountId) {
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce compte ? Tous les trades associés seront supprimés.')) {
        return;
    }
    
    try {
        const api = new API();
        await api.deleteAccount(accountId);
        showToast('Compte supprimé avec succès', 'success');
        loadAccounts();
    } catch (error) {
        console.error('Error deleting account:', error);
        showToast('Erreur lors de la suppression du compte', 'error');
    }
}

/**
 * Render comparison chart
 */
function renderComparisonChart() {
    if (comparisonChart) comparisonChart.destroy();
    
    if (accounts.length < 2) return;
    
    const colors = ['#3B82F6', '#8B5CF6', '#00D26A', '#F59E0B', '#FF4757'];
    
    const series = accounts.slice(0, 5).map((account, index) => {
        // Generate equity curve for each account (simplified)
        const equityData = [];
        let balance = account.initial_balance;
        
        for (let i = 0; i < 30; i++) {
            balance += (Math.random() - 0.4) * 100; // Random P&L
            equityData.push({
                x: i,
                y: balance
            });
        }
        
        return {
            name: account.name,
            data: equityData
        };
    });
    
    const options = {
        series: series,
        chart: {
            type: 'line',
            height: 400,
            fontFamily: 'Inter, sans-serif',
            background: 'transparent',
            toolbar: { show: true }
        },
        colors: colors,
        stroke: { curve: 'smooth', width: 2 },
        xaxis: {
            type: 'numeric',
            title: { text: 'Jours', style: { color: '#8B9AB1' } },
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
        },
        legend: {
            position: 'top',
            labels: { colors: '#8B9AB1' }
        }
    };
    
    comparisonChart = new ApexCharts(document.getElementById('comparisonChart'), options);
    comparisonChart.render();
}

/**
 * Render comparison table
 */
function renderComparisonTable() {
    const tbody = document.getElementById('comparisonTableBody');
    
    if (accounts.length < 2) return;
    
    const account1 = accounts[0];
    const account2 = accounts[1];
    
    document.getElementById('comparisonHeader1').textContent = account1.name;
    document.getElementById('comparisonHeader2').textContent = account2.name;
    
    // Calculate metrics for each account (simplified)
    const calculateMetrics = (account) => {
        const totalPnL = account.current_balance - account.initial_balance;
        const winRate = 45 + Math.random() * 20; // Placeholder
        const avgRR = 1.0 + Math.random() * 1.5; // Placeholder
        const profitFactor = 1.2 + Math.random() * 0.8; // Placeholder
        const trades = Math.floor(Math.random() * 100) + 10; // Placeholder
        
        return { totalPnL, winRate, avgRR, profitFactor, trades };
    };
    
    const metrics1 = calculateMetrics(account1);
    const metrics2 = calculateMetrics(account2);
    
    const metrics = [
        { name: 'Solde Actuel', key: 'current_balance', format: v => formatCurrency(v) },
        { name: 'P&L Total', key: 'totalPnL', format: v => formatCurrency(v) },
        { name: 'Win Rate', key: 'winRate', format: v => `${v.toFixed(1)}%` },
        { name: 'RR Moyen', key: 'avgRR', format: v => v.toFixed(2) },
        { name: 'Profit Factor', key: 'profitFactor', format: v => v.toFixed(2) },
        { name: 'Nb Trades', key: 'trades', format: v => v }
    ];
    
    tbody.innerHTML = metrics.map(metric => {
        const value1 = metric.key === 'current_balance' ? account1[metric.key] : metrics1[metric.key];
        const value2 = metric.key === 'current_balance' ? account2[metric.key] : metrics2[metric.key];
        
        return `
            <tr>
                <td><strong>${metric.name}</strong></td>
                <td>${metric.format(value1)}</td>
                <td>${metric.format(value2)}</td>
            </tr>
        `;
    }).join('');
}

/**
 * Update account selector
 */
function updateAccountSelector() {
    const selector = document.getElementById('activeAccount');
    selector.innerHTML = accounts.map(a => `<option value="${a.id}">${a.name}</option>`).join('');
}

/**
 * Handle account change
 */
function onAccountChange(accountId) {
    selectedAccount = accounts.find(a => a.id === parseInt(accountId));
    if (selectedAccount && selectedAccount.type === 'PROP_FIRM') {
        showPropFirmDashboard(selectedAccount);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    initializeCommon();
    initializeAccounts();
});
