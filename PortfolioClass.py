import GetData
import time
from sys import exit

class Portfolio:

    def __init__(self, tickersymbolist, inputdate_init, inputdate_fin, initialcapital):

        self.initialcapital = initialcapital
        self.transactioncost = 0.5
        #self.pershare_transactioncost = 0.005
        self.availablecapital = self.initialcapital
        self.inputdate_init = inputdate_init
        self.inputdate_fin = inputdate_fin
        self.tickersymbolist = tickersymbolist
        self.portfolio = []

        for c in range(len(tickersymbolist)):
            company = self.Company(tickersymbolist[c])
            self.portfolio.append(company)

        #Get Open price data for all Ticker Symbols in one DataFrame - from 3 years before inputdate_init to inputdate_fin
        self.pricedatadf, self.simulationdf = GetData.getpricedatadf(self.tickersymbolist, self.portfolio, self.inputdate_init, self.inputdate_fin, 3)

    def getportfoliovalue(self, dfindex):
        totalcapital = 0
        for company in self.portfolio:
            totalcapital += company.capital
            if company.stocks > 0:
                sell = company.stocks * (self.simulationdf['Price' + company.ticker][dfindex])
                totalcapital += sell - self.transactioncost

        totalcapital += self.availablecapital

        return totalcapital

    def printportfolio(self):
        print('----PORTFOLIO-----')
        for c in self.portfolio:
            print(c)
        print('Remaining Capital:')
        print(self.availablecapital)
        return '------------------'

    def __str__(self):
        return self.printportfolio()

    def __getitem__(self, str_ticker):
        try:
            iticker = self.tickersymbolist.index(str_ticker)
        except ValueError:
            print('No TickerSymbol: ' + str_ticker)
            exit()
        return self.portfolio[iticker]


    class Company:
        def __init__(self, ticker):
            self.ticker = ticker
            self.stocks = 0
            self.capital = 0
            self.datadf = GetData.getdfdata(ticker)

        def __str__(self):
            return "Ticker -> %s \t; Stocks -> %s \t; Capital-> %s" % (self.ticker, self.stocks, self.capital)

