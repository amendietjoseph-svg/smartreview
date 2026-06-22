const BASE_URL = window.location.hostname === 'localhost'
  ? 'http://localhost:8001'
  : 'https://smartreview-production-951d.up.railway.app';

class API {
  static async request(method, endpoint, data = null) {
    try {
      const options = {
        method,
        headers: { 'Content-Type': 'application/json' },
      };
      if (data) options.body = JSON.stringify(data);
      const response = await fetch(`${BASE_URL}${endpoint}`, options);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return await response.json();
    } catch (error) {
      console.error(`API Error ${method} ${endpoint}:`, error);
      throw error;
    }
  }

  static async getAccounts() {
    return await this.request('GET', '/api/accounts');
  }
  static async createAccount(data) {
    return await this.request('POST', '/api/accounts', data);
  }
  static async updateAccount(id, data) {
    return await this.request('PUT', `/api/accounts/${id}`, data);
  }
  static async deleteAccount(id) {
    return await this.request('DELETE', `/api/accounts/${id}`);
  }
  static async getTrades(accountId = null, period = null) {
    let url = '/api/trades';
    const params = [];
    if (accountId) params.push(`account_id=${accountId}`);
    if (period) params.push(`period=${period}`);
    if (params.length) url += '?' + params.join('&');
    return await this.request('GET', url);
  }
  static async createTrade(data) {
    return await this.request('POST', '/api/trades', data);
  }
  static async updateTrade(id, data) {
    return await this.request('PUT', `/api/trades/${id}`, data);
  }
  static async deleteTrade(id) {
    return await this.request('DELETE', `/api/trades/${id}`);
  }
  static async getStats(accountId = null, period = null) {
    let url = '/api/stats';
    const params = [];
    if (accountId) params.push(`account_id=${accountId}`);
    if (period) params.push(`period=${period}`);
    if (params.length) url += '?' + params.join('&');
    return await this.request('GET', url);
  }
  static async checkHealth() {
    try {
      const response = await fetch(`${BASE_URL}/`);
      return response.ok;
    } catch {
      return false;
    }
  }
}
