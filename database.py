def GetConnectionString():
    DRIVER_NAME = '{ODBC Driver 17 for SQL Server}'
    SERVER_NAME = 'DESKTOP-9IO0POK\SQLEXPRESS'
    DATABASE_NAME = 'FMP-API'

    connectionString = 'DRIVER=' + DRIVER_NAME + ';SERVER=' + SERVER_NAME + ';DATABASE=' + DATABASE_NAME + ';trusted_connection=yes'

    return connectionString

    