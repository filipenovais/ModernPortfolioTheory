import pandas as pd
import talib as ta
import numpy as np
import os.path
import os
import time
import datetime
from sys import exit
import pandas_datareader.data as web
import datetime as dt

import PortfolioClass
#import Crypto


# Get Open price data for all Ticker Symbols in one DataFrame
def getpricedatadf(tickersymbolist, portfolio, inputdate_init, inputdate_fin, numberoftrainingyears):
    pricedatadf = pd.DataFrame()
    for i in range(len(tickersymbolist)):
        df_ticker = portfolio[i].datadf

        # Get 'Open' column, change name and joint to existing DataFrame
        datadfaux = df_ticker['Open']
        datadfaux = pd.DataFrame(data=datadfaux)
        datadfaux.columns = ['Price' + str(portfolio[i].ticker)]
        pricedatadf = pricedatadf.join(datadfaux, how='outer')

        # Check Nan values after join
        if pricedatadf.isnull().values.any():
            print('Check nan values on ********** ' + str(portfolio[i].ticker) + ' **********')
            #exit()

    # Slice DataFrame 3 years before inputdate_init
    # get first simulation day and subtract numberoftrainingyears
    fixedday = pd.to_datetime(inputdate_init).day
    fixedmonth = pd.to_datetime(inputdate_init).month
    trainindex = pd.to_datetime(inputdate_init)
    trainindex = trainindex.replace(year=trainindex.year-numberoftrainingyears, month=fixedmonth, day=fixedday)

    # get slicedf to use during the simulation
    if inputdate_fin == 'now':
        sliceddf = pricedatadf[trainindex:]
        simulationdf = pricedatadf[inputdate_init:]
    else:
        sliceddf = pricedatadf[trainindex:inputdate_fin]
        simulationdf = pricedatadf[inputdate_init:inputdate_fin]

    # Check Nan values in the Price DataFrame
    if sliceddf.isnull().values.any():
        print('Check DataFrame Nan Values')
        exit()

    return sliceddf, simulationdf

# Download TickerSymbol DataFrame
def getdfdata (TickerSymbol):

    if not os.path.exists('tickercsv/'):
        os.makedirs('tickercsv/')

    if not os.path.exists('tickercsv/'+ TickerSymbol + '.csv'):
        #print('Downloading '+ TickerSymbol +' Data. Check CSV directory')
        downloaddata = 1
    else:
        #print('tickercsv/' + TickerSymbol + '.csv Data')
        downloaddata = 0

    # debug (always downloaddata=??)
    print('Downloading ' + TickerSymbol + ' Data. Check CSV directory')
    downloaddata = 1
    if downloaddata:
        start = dt.datetime(2014, 1, 1)

        #end = dt.datetime(2019, 1, 1)
        end = dt.datetime.now()
        try:
            # Get Daily Data from yahoo
            df = web.DataReader(TickerSymbol, "yahoo", start, end)
            # Get Monthly Data from yahoo
            #df = web.get_data_yahoo(TickerSymbol, start, interval = 'm')

            # save DataFrame in tickercsv folder
            df.to_csv('tickercsv/' + str(TickerSymbol) + '.csv')
            df_csv = pd.read_csv('tickercsv/' + TickerSymbol + '.csv', parse_dates=True, index_col=0)

            # Remove 'Close' from results
            # df_csv = df_csv.drop(['Close'], axis=1)
            df_csv.Volume = df_csv.Volume.astype(float)
            pass

        except Exception as e:
            print('WrongTickerERROR: Couldnt download data---------------------------------------------------------------')
            print(TickerSymbol)
            df_empty = pd.DataFrame({'EmptyDataframe': []})
            exit()
    else:
        # Read csv
        df_csv = pd.read_csv('tickercsv/'+ TickerSymbol + '.csv', parse_dates=True, index_col=0)

        # Remove 'Close' from results
        #df_csv = df_csv.drop(['Close'], axis=1)
        df_csv.Volume = df_csv.Volume.astype(float)

    # Datetime index
    df_csv.index = pd.to_datetime(df_csv.index)
    return df_csv



# Get User input
def askinput():
    #ASK DOR DATE
    inputdate_init = input("Enter Initial Simulation Date (YYYY-MM-DD) ")
    inputdate_init = validate_date(inputdate_init)
    inputdate_fin = input("Enter Final Simulation Date (YYYY-MM-DD or 'now') ")
    inputdate_fin = validate_date(inputdate_fin)

    # ASK FOR TICKER
    tickersymbolist = []
    doneTicker = 0
    while doneTicker == 0:
        inputTickerSymbol = input("Select company Ticker: ")
        inputTickerSymbol = validate_ticker(inputTickerSymbol)

        if inputTickerSymbol == '1':
            break
        tickersymbolist.append(inputTickerSymbol.upper())
        print('Current Symbols ->  ' + str(tickersymbolist))

    return inputdate_init, inputdate_fin, tickersymbolist

# Check for errors on Date
def validate_date(inputdate):
    while True:
        try:
            datetime.datetime.strptime(inputdate, '%Y-%m-%d')
            return inputdate
        except ValueError:
            print('Incorrect date, should be YYYY-MM-DD')
            print('Try again? (exit system -> 0')
            inputdate = input()
            if inputdate == '0':
                exit()

# Check for errors on Ticker
def validate_ticker(inputTicker):
    if inputTicker == '1':
        return '1'

    start = dt.datetime(2019, 1, 1)
    end = dt.datetime(2019, 2, 1)

    while True:
        try:
            print('Checking Ticker...')
            df = web.DataReader(inputTicker, "yahoo", start, end)
            print('Correct Ticker Symbol!! Finish -> 1')
            return inputTicker
        except Exception as e:
            print('Incorrect Ticker')
            print('Try again? (exit system -> 0 ; finish -> 1)')
            inputTicker = input()
            if inputTicker == '0':
                exit()
            elif inputTicker == '1':
                return '1'
