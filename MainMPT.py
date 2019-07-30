import GetData
import MinVar
import Market
import ProcessData
import PortfolioClass

import time
import datetime
import pandas as pd
from sys import exit



# Get User input
# !!!!!! inputdate_init >= '2017-01-01' !!!!!!
#inputdate_init, inputdate_fin, tickersymbolist = GetData.askinput()


# !!!!!! inputdate_init >= '2017-01-01' !!!!!!
inputdate_init = '2018-06-01'
#inputdate_fin = '2018-09-01'
inputdate_fin = 'now'

#tickersymbolist = ['BTC', 'LTC', 'ETH']
tickersymbolist = ['AAPL', 'MSFT', 'FB']

# Initial Capital
initialcapital = 10000
pershare_transactioncost = 0.005
transactioncost = 0.5

# Create portfolio
portfolio = PortfolioClass.Portfolio(tickersymbolist, inputdate_init, inputdate_fin, initialcapital)
#portfolio['MSFT'].stocks = 5
print(portfolio)

# Simulation input date begin
print(inputdate_init)
# Simulation input date final
print(inputdate_fin)
# List of Ticker Symbols
print(tickersymbolist)
print()

# Check Open Market days in input Dates
simdate_init = portfolio.pricedatadf[inputdate_init:].index[0]
simdate_fin = portfolio.pricedatadf[inputdate_init:].index[-1]
print('Simulation begin and finish:')
print(simdate_init)
print(simdate_fin)

# Minimum Variance Portfolio
weightsdf = MinVar.main(portfolio)

Market.main(portfolio, weightsdf)

exit()