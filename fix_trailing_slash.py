with open('frontend/js/api.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Ajouter slash final sur toutes les routes pour eviter la redirection
c = c.replace("return await this.request('GET', '/api/accounts');", "return await this.request('GET', '/api/accounts/');")
c = c.replace("return await this.request('POST', '/api/accounts', data);", "return await this.request('POST', '/api/accounts/', data);")
c = c.replace("let url = '/api/trades';", "let url = '/api/trades/';")
c = c.replace("return await this.request('POST', '/api/trades', data);", "return await this.request('POST', '/api/trades/', data);")
c = c.replace("let url = '/api/stats';", "let url = '/api/stats/';")

with open('frontend/js/api.js', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done!')