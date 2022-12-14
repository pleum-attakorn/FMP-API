from pymongo import MongoClient
import certifi
import pandas as pd
import requests

api_key = pd.read_csv('../key.txt', header=None)[0][0]
URL = 'https://financialmodelingprep.com/api/v3/'
data = 'delisted-companies'

ca = certifi.where()
myclient = MongoClient("mongodb+srv://pleum:1234@cluster0.vyv4b.mongodb.net/test?retryWrites=true&w=majority", tlsCAFile = ca)
db = myclient['FMP-API']
mycoll = db['Delisted_Companies']
mycoll.delete_many({})

api_key = pd.read_csv('../key.txt', header=None)[0][0]
URL = 'https://financialmodelingprep.com/api/v3/'
data = 'delisted-companies'

# page = 0
# r = requests.get('{}{}?page={}&apikey={}'.format(URL, data, page, api_key))
# df2 = pd.DataFrame.from_dict(r.json())
# for i in range(0, len(df2)):
#     lst = list(df2.iloc[i])
#     mycoll.insert_one({'_id': i, 'symbol' : lst[0],  'companyName' : lst[1], 'exchange' : lst[2], 'ipoDate': lst[3], 'delistedDate': lst[4]})

df = pd.DataFrame()
for i in range(0, 57):
    page = i
    r = requests.get('{}{}?page={}&apikey={}'.format(URL, data, page, api_key))
    df2 = pd.DataFrame.from_dict(r.json())
    df = pd.concat([df, df2])
df.reset_index(drop=True, inplace=True)
for i in range(0, len(df)):
    lst = list(df.iloc[i])
    mycoll.insert_one({'_id': i, 'symbol' : lst[0],  'companyName' : lst[1], 'exchange' : lst[2], 'ipoDate': lst[3], 'delistedDate': lst[4]})
    

