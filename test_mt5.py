import MetaTrader5 as mt5
import os
from dotenv import load_dotenv
load_dotenv(r'C:\Users\amend\OneDrive\Desktop\CATHERINE AI\backend\.env')

login = int(os.getenv('MT5_LOGIN'))
password = os.getenv('MT5_PASSWORD')
server = os.getenv('MT5_SERVER')

print(f'Connecting to {server} with login {login}...')

if not mt5.initialize():
    print(f'MT5 init failed: {mt5.last_error()}')
    exit()

authorized = mt5.login(login, password=password, server=server)
if authorized:
    info = mt5.account_info()
    print(f'Connected!')
    print(f'Name: {info.name}')
    print(f'Balance: {info.balance} {info.currency}')
    print(f'Equity: {info.equity}')
    print(f'Server: {info.server}')
else:
    print(f'Login failed: {mt5.last_error()}')

mt5.shutdown()
