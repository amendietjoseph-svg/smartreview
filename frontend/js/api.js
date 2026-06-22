/**
 * API client for SmartReview backend
 * Handles all HTTP requests to the FastAPI server
 */

class API {
    constructor() {
        this.BASE_URL = window.location.hostname === 'localhost'
            ? 'http://localhost:8001'
            : 'https://smartreview-api.up.railway.app';
    }

    /**
     * Generic request method with error handling
     */
    async request(endpoint, options = {}) {
        try {
            const url = `${this.BASE_URL}${endpoint}`;
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`API Error (${endpoint}):`, error);
            throw error;
        }
    }

    /**
     * Trade operations
     */
    async getTrades(accountId = null, skip = 0, limit = 100) {
        let endpoint = `/api/trades/?skip=${skip}&limit=${limit}`;
        if (accountId) {
            endpoint += `&account_id=${accountId}`;
        }
        return this.request(endpoint);
    }

    async getTrade(tradeId) {
        return this.request(`/api/trades/${tradeId}`);
    }

    async createTrade(tradeData) {
        return this.request('/api/trades/', {
            method: 'POST',
            body: JSON.stringify(tradeData)
        });
    }

    async updateTrade(tradeId, tradeData) {
        return this.request(`/api/trades/${tradeId}`, {
            method: 'PUT',
            body: JSON.stringify(tradeData)
        });
    }

    async deleteTrade(tradeId) {
        return this.request(`/api/trades/${tradeId}`, {
            method: 'DELETE'
        });
    }

    /**
     * Statistics operations
     */
    async getStats(accountId, period = 'all') {
        return this.request(`/api/stats/account/${accountId}?period=${period}`);
    }

    async getEquityCurve(accountId, period = 'all') {
        return this.request(`/api/stats/equity/${accountId}?period=${period}`);
    }

    async getPerformanceMetrics(accountId) {
        return this.request(`/api/stats/performance/${accountId}`);
    }

    /**
     * Account operations
     */
    async getAccounts(skip = 0, limit = 100) {
        return this.request(`/api/accounts/?skip=${skip}&limit=${limit}`);
    }

    async getActiveAccounts() {
        return this.request('/api/accounts/active');
    }

    async getAccount(accountId) {
        return this.request(`/api/accounts/${accountId}`);
    }

    async createAccount(accountData) {
        return this.request('/api/accounts/', {
            method: 'POST',
            body: JSON.stringify(accountData)
        });
    }

    async updateAccount(accountId, accountData) {
        return this.request(`/api/accounts/${accountId}`, {
            method: 'PUT',
            body: JSON.stringify(accountData)
        });
    }

    async deleteAccount(accountId) {
        return this.request(`/api/accounts/${accountId}`, {
            method: 'DELETE'
        });
    }

    /**
     * AI Coach operations
     */
    async getAIAnalysis(accountId, period = '30d') {
        return this.request('/api/ai/analyze', {
            method: 'POST',
            body: JSON.stringify({
                account_id: accountId,
                period: period
            })
        });
    }

    async getEdgeTracker(accountId) {
        return this.request(`/api/ai/edge/${accountId}`);
    }

    /**
     * Health check
     */
    async healthCheck() {
        try {
            return await this.request('/');
        } catch (error) {
            return null;
        }
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API;
}
