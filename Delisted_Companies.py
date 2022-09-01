import pandas as pd
import requests
import pyodbc
import database

api_key = pd.read_csv('./key.txt', header=None)[0][0]
URL = 'https://financialmodelingprep.com/api/v3/'
data = 'delisted-companies'
#page = 0

con_str = database.GetConnectionString()

def create_table():
    sql = '''
        CREATE TABLE Delisted_Companies (symbol varchar(255),companyName varchar(255), exchange varchar(255), ipoDate DATE, delistedDate DATE)
    '''
    with pyodbc.connect(con_str) as con:
        cursor = con.cursor()
        cursor.execute(sql)
        cursor.close()

def check_table():
    sql = '''
        SELECT COUNT(*) FROM information_schema.tables
        WHERE table_name = 'Delisted_Companies'
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
        DELETE FROM Delisted_Companies
    '''
    with pyodbc.connect(con_str) as con:
        cursor = con.cursor()
        cursor.execute(sql)
        cursor.close()

def insert_data(data):
    sql = '''
        INSERT INTO Delisted_Companies VALUES (?, ?, ?, ?, ?)
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
    
    df = pd.DataFrame()
    for i in range(0, 57):
        page = i
        r = requests.get('{}{}?page={}&apikey={}'.format(URL, data, page, api_key))
        df2 = pd.DataFrame.from_dict(r.json())
        df = pd.concat([df, df2])
    
    df.reset_index(drop=True, inplace=True)
    insert_data(df.values.tolist())