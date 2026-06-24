with open('frontend/js/api.js', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace("return await this.request('GET', '/accounts');", "return await this.request('GET', '/api/accounts');")
c = c.replace("return await this.request('POST', '/accounts', data);", "return await this.request('POST', '/api/accounts', data);")
c = c.replace("return await this.request('PUT', `/accounts/${id}`, data);", "return await this.request('PUT', `/api/accounts/${id}`, data);")
c = c.replace("return await this.request('DELETE', `/accounts/${id}`);", "return await this.request('DELETE', `/api/accounts/${id}`);")
c = c.replace("let url = '/trades';", "let url = '/api/trades';")
c = c.replace("return await this.request('POST', '/trades', data);", "return await this.request('POST', '/api/trades', data);")
c = c.replace("return await this.request('PUT', `/trades/${id}`, data);", "return await this.request('PUT', `/api/trades/${id}`, data);")
c = c.replace("return await this.request('DELETE', `/trades/${id}`);", "return await this.request('DELETE', `/api/trades/${id}`);")
c = c.replace("let url = '/stats';", "let url = '/api/stats';")

with open('frontend/js/api.js', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')
print(open('frontend/js/api.js').read())