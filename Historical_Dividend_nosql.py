from pymongo import MongoClient
import certifi
import pandas as pd
import requests

api_key = pd.read_csv('../key.txt', header=None)[0][0]
URL = 'https://financialmodelingprep.com/api/v3/'
data = 'historical-price-full/stock_dividend/'

ca = certifi.where()
myclient = MongoClient(pd.read_csv('../key.txt', header=None)[0][3], tlsCAFile = ca)
db = myclient['FMP-API']
mycoll = db['Historical_Dividend']
mycoll.delete_many({})

# data = mycoll.find({})
# print(list(data))

ticker = 'AAPL'
r = requests.get('{}{}{}?apikey={}'.format(URL, data, ticker, api_key))
df = pd.json_normalize(r.json()['historical'])
df['symbol'] = ticker
cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols]

for i in range(0, len(df)):
    lst = list(df.iloc[i])
    mycoll.insert_one({'_id': i, 'symbol' : lst[0],  'date' : lst[1], 'label' : lst[2], 'adjDividend': lst[3], 'dividend': lst[4], 'recordDate': lst[5], 'paymentDate': lst[6], 'declarationDate': lst[7]})
    