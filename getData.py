import pandas as pd
import requests

api_key = pd.read_csv('./key.txt', header=None)[0][0]
#tickers = ['AAPL']

URL = 'https://financialmodelingprep.com/api/v3/'
data = 'delisted-companies'
page = 0

r = requests.get('{}{}?page={}&apikey={}'.format(URL, data, page, api_key))

df = pd.DataFrame.from_dict(r.json())

print(df.head())