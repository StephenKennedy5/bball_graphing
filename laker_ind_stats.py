import json
import pandas as pd

def laker_roster():
    with open('laker_players.json') as f:
      data = json.load(f)
    laker_key = list(data.keys())
    laker_url = list(data.values())
    f.close()
    return laker_url, laker_key

def pds_html(laker_url,laker_key):
    for i in range(len(laker_url)):
        data = pd.read_html(laker_url[i],skiprows=(21,42,63))
        data = data[-1]
        data.to_csv(laker_key[i]+'_data.csv',index=False)

laker_url,laker_key = laker_roster()
pds_html(laker_url,laker_key)
