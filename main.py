import datetime
import time

import pandas as pd
import requests

import schedule

address = "0x4Ce8b6532ECfeF3B5574b83B13d6366f40D2837f"
api_key = 'R3BFP5XNC7HGMM6XB7APPHFBGIXAZJ7SRU'

url = "https://api.etherscan.io/api"

params = {
    "module": "account",
    "action": "balancemulti",
    "address": f'{address}',
    "tag": "account",
    "apikey": api_key,
}
response = requests.get(url, params=params)
data = response.json()

balance = float(data['result'][0]['balance'])/10**18
print(f'Balance: {balance}')


def func():
    params = {
        "module": "gastracker",
        "action": "gasoracle",
        "apikey": api_key,
    }

    ges_response = requests.get(url, params=params)
    ges_data = ges_response.json()

    date = datetime.datetime.now().date()

    fast = ges_data['result']['FastGasPrice']
    safe = ges_data['result']['SafeGasPrice']
    proporse = ges_data['result']['ProposeGasPrice']

    ges_df = pd.DataFrame({
        'date': [date],
        'fast': [fast],
        'proporse': [proporse],
        'safe': [safe]
    })

    print(ges_df)

    with open('ges.csv', 'a') as f:
        ges_df.to_csv(f, header=False, index=False)

    stats_url = "https://api.etherscan.io/api"
    stats_params = {
        "module": "stats",
        "action": "ethsupply",
        "apikey": 'R3BFP5XNC7HGMM6XB7APPHFBGIXAZJ7SRU',
    }

    node_resp = requests.get(stats_url, params=stats_params)
    node_data = node_resp.json()

    total_supply = node_data['result']
    print("Total Supply: {}".format(total_supply))

    node_df = pd.DataFrame()

    node_df.to_csv('nodes.csv', index=False)


# Run the bot immediately
func()

schedule.every(20).seconds.do(func)
while True:
    try:
        schedule.run_pending()
        time.sleep(15)
    except Exception as e:
        print('Error:', str(e))
        time.sleep(30)
