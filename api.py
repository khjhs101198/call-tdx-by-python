import auth
import requests
import json
import time

# 請求標頭
headers = {
    'Authorization': 'Bearer ' + auth.token,
    'Accept-Encoding': 'gzip',
}

# 呼叫API
def call(url, params, file_name):
    # 發送請求
    r = requests.get(url, params=params, headers=headers, stream=True)

    # 檢查是否成功取得資料
    if r.status_code == 200:
        print('成功取得資料')

        current_timestamp = int(time.time())

        # 將資料寫入檔案
        if '$format' in params and params['$format'] == 'JSONL':
            with open(f'./data/{file_name}_{current_timestamp}.jsonl', 'w', encoding='utf-8') as f:
                # for line in r.iter_lines(decode_unicode=True):
                #     if line:
                #         f.write(line + "\n")
                for line in r.iter_lines():
                    if line:
                        f.write(line.decode('utf-8-sig') + "\n")
                # for item in [json.loads(line) for line in r.content.decode('utf-8-sig').splitlines()]:
                #     json.dump(item, f, indent=4, ensure_ascii=False)
                #     f.write('\n')
        else:
            with open(f'./data/{file_name}_{current_timestamp}.json', 'w', encoding='utf-8') as f:
                json.dump(r.json(), f, indent=4, ensure_ascii=False)
    elif r.status_code == 249:
        print('取得統計資料:', r.text)
    else:
        print('取得資料失敗:', r.text)