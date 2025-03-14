import os
import requests
from dotenv import load_dotenv
from diskcache import Cache

# 取得token的URL
AUTH_URL = 'https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token'

# 讀取.env檔案
load_dotenv()

# 檢查是否有設定環境變數
if os.environ.get('CLIENT_ID') is None or os.environ.get('CLIENT_SECRET') is None:
    raise Exception("請在.env檔案中設定CLIENT_ID和CLIENT_SECRET")

# 建立快取
cache = Cache('./my_cache')

# 從cache中取得token
token = cache.get('token')

# 檢查token是否過期，若過期則重新取得
if token is None:
    auth_data = {
        'grant_type': 'client_credentials',
        'client_id': os.environ.get('CLIENT_ID'),
        'client_secret': os.environ.get('CLIENT_SECRET')
    }

    r = requests.post(AUTH_URL, data=auth_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})

    json_data = r.json()

    if r.status_code == 200:
        print('成功取得token:', json_data)

        cache.set('token', json_data['access_token'], expire=json_data['expires_in'] - 60)

        token = json_data['access_token']
    else:
        print('取得token失敗:', r.text)
        
# 關閉快取
cache.close()