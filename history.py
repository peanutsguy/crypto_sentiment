import requests
import datetime
import secrets
import json

def get_historical_data(days,crypto = "btc"):
    start_time = datetime.datetime.now() - datetime.timedelta(days=days)
    payload = {
        "period_id"  : "1DAY",
        "time_start" : start_time.strftime("%Y-%m-%dT%X"),
        "time_end"   : datetime.datetime.now().strftime("%Y-%m-%dT%X"),
    }
    headers = {'X-CoinAPI-Key' : secrets.cryptokey}
    url = 'https://rest.coinapi.io/v1/exchangerate/'+crypto.upper()+'/USD/history'
    response = requests.get(url, headers=headers, params=payload)
    return response

data = get_historical_data(30,"eth").text

a = json.loads(data)

d = []

for entry in a:
    d.append((entry["rate_high"]+entry["rate_low"])/2)

window_size = 7

for i in range(len(d) - window_size + 1):
    print(sum(d[i: i + window_size])/window_size)
