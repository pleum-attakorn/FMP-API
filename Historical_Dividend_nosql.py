from pymongo import MongoClient
import certifi
import pandas as pd
import requests

api_key = pd.read_csv('../key.txt', header=None)[0][0]
URL = 'https://financialmodelingprep.com/api/v3/'
data = 'historical-price-full/stock_dividend/'

ca = certifi.where()

def get_symbol():
    DC_client = MongoClient(pd.read_csv('../key.txt', header=None)[0][3], tlsCAFile = ca)
    db = DC_client['FMP-API']
    DC_coll = db['Delisted_Companies']

    data = DC_coll.find({})
    lst_data = list(data)
    symbol = []
    for i in range(0, len(lst_data)):
        symbol.append(lst_data[i]['symbol'])
    return symbol

if __name__ == '__main__':
    symbol = get_symbol()
    count = 0
    df = pd.DataFrame()

    for i in symbol:
        if count >= 10:
            break
        ticker = i
        r = requests.get('{}{}{}?apikey={}'.format(URL, data, ticker, api_key))
        if (bool(r.json())):
            df2 = pd.json_normalize(r.json()['historical'])
            df2['symbol'] = ticker
            cols = df2.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            df2 = df2[cols]
            df = pd.concat([df, df2])
        count = count + 1
    df.reset_index(drop=True, inplace=True)

    myclient = MongoClient(pd.read_csv('../key.txt', header=None)[0][3], tlsCAFile = ca)
    db = myclient['FMP-API']
    mycoll = db['Historical_Dividend']
    mycoll.delete_many({})

    for i in range(0, len(df)):
        lst = list(df.iloc[i])
        mycoll.insert_one({'_id': i, 'symbol' : lst[0],  'date' : lst[1], 'label' : lst[2], 'adjDividend': lst[3], 'dividend': lst[4], 'recordDate': lst[5], 'paymentDate': lst[6], 'declarationDate': lst[7]})

# ticker = 'AAPL'
# r = requests.get('{}{}{}?apikey={}'.format(URL, data, ticker, api_key))
# df = pd.json_normalize(r.json()['historical'])
# df['symbol'] = ticker
# cols = df.columns.tolist()
# cols = cols[-1:] + cols[:-1]
# df = df[cols]

# for i in range(0, len(df)):
#     lst = list(df.iloc[i])
#     mycoll.insert_one({'_id': i, 'symbol' : lst[0],  'date' : lst[1], 'label' : lst[2], 'adjDividend': lst[3], 'dividend': lst[4], 'recordDate': lst[5], 'paymentDate': lst[6], 'declarationDate': lst[7]})
