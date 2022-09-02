# FMP-API

I have save my api key of FMP API, the detail about my sql server and the link to my MongoDB Clound in key.txt file so if you want to run these program change those detail to your key.

Delisted_Companies : Get data about Delisted Companies from page 0 to page 56 and save it to sql server, need to do this before Historical Dividend because we will get each stock symbol from Delisted Companies data.

Historical_Dividend : Get each stock symbol from Delisted Companies data then get and save data about Historical Dividend for each symbol that has these data. Because the request has limit time to use, I can't get all data from in one run so I have limit it to 10 time.

Delisted_Companies_nosql : same as Delisted_Companies but save it to NoSQL database instead (MongoDB Clound)

Historical_Dividend_nosql : same as Historical_Dividend but save it to NoSQL database instead (MongoDB Clound)

database : get the connection string to FMP API