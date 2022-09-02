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
    
def create_table():
    sql = '''
        CREATE TABLE Historical_Dividend (symbol varchar(255),y_m_d DATE, label varchar(255), adjDividend FLOAT(6), dividend FLOAT(2),
        recordDate DATE, paymentDate DATE, declarationDate DATE)
    '''
    with pyodbc.connect(con_str) as con:
        cursor = con.cursor()
        cursor.execute(sql)
        cursor.close()

def check_table():
    sql = '''
        SELECT COUNT(*) FROM information_schema.tables
        WHERE table_name = 'Historical_Dividend'
    '''
    with pyodbc.connect(con_str) as con:
        cursor = con.cursor()
        cursor.execute(sql)
        if cursor.fetchone()[0] == 1:
            cursor.close()
            return True
        else:
            cursor.close()
            return False

def clear_data():
    sql = '''
        DELETE FROM Historical_Dividend
    '''
    with pyodbc.connect(con_str) as con:
        cursor = con.cursor()
        cursor.execute(sql)
        cursor.close()

def insert_data(data):
    sql = '''
        INSERT INTO Historical_Dividend VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    '''
    with pyodbc.connect(con_str) as con:
        cursor = con.cursor()
        cursor.executemany(sql, data)
        cursor.close()

if __name__ == '__main__':

    if(check_table()):
        clear_data()
    else:
        create_table()
    
    # ticker = 'AAPL'
    # r = requests.get('{}{}{}?apikey={}'.format(URL, data, ticker, api_key))
    # df = pd.json_normalize(r.json()['historical'])
    # df['symbol'] = ticker
    # cols = df.columns.tolist()
    # cols = cols[-1:] + cols[:-1]
    # df = df[cols]
    # insert_data(df.values.tolist())

    symbol = select_symbol()
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
    insert_data(df.values.tolist())

    
    