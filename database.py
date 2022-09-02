import pandas as pd

def GetConnectionString():
    DRIVER_NAME = pd.read_csv('../key.txt', header=None)[0][1]
    SERVER_NAME = pd.read_csv('../key.txt', header=None)[0][2]
    DATABASE_NAME = 'FMP-API'

    connectionString = 'DRIVER=' + DRIVER_NAME + ';SERVER=' + SERVER_NAME + ';DATABASE=' + DATABASE_NAME + ';trusted_connection=yes'

    return connectionString

    