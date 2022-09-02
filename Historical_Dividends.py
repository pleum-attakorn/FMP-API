import pandas as pd
import requests
import pyodbc
import database

api_key = pd.read_csv('../key.txt', header=None)[0][0]
URL = 'https://financialmodelingprep.com/api/v3/'
data = 'historical-price-full/stock_dividend/'

con_str = database.GetConnectionString()

def select_symbol():
    sql = '''
        SELECT symbol
        FROM Delisted_Companies
    '''    
    with pyodbc.connect(con_str) as con:
        cursor = con.cursor()
        lst = []
        for row in cursor.execute(sql):
            lst.append(row[0])
        cursor.close()
        return lst
    

if __name__ == '__main__':

    symbol = select_symbol()
    ticker = 'AAPL'
    print(symbol[0])
    #r = requests.get('{}{}{}?apikey={}'.format(URL, data, ticker, api_key))
    #print(bool(r.json()))
    # df2 = pd.json_normalize(r.json()['historical'])
    # df2['symbol'] = ticker
    # cols = df2.columns.tolist()
    # cols = cols[-1:] + cols[:-1]
    # df2 = df2[cols]
    # print(df2)
    