import PortfolioClass

import pandas as pd
from scipy.optimize import minimize
import numpy as np
from sys import exit

from matplotlib import pyplot as plt
from matplotlib import style, gridspec
import matplotlib.dates as mdates


def buystocks(portfolio, dfindex):
    transactioncost = 0.5
    pershare_transactioncost = 0.005

    for ticker in portfolio.tickersymbolist:
        stockstobuy = portfolio[ticker].capital // (portfolio.simulationdf['Price' + ticker][dfindex] + pershare_transactioncost)
        if stockstobuy > 0:
            buy = stockstobuy * (portfolio.simulationdf['Price' + ticker][dfindex] + pershare_transactioncost)
            portfolio[ticker].capital -= buy + transactioncost
            portfolio[ticker].stocks = stockstobuy

    return portfolio

def sellstocks(portfolio, dfindex):
    transactioncost = 0.5
    pershare_transactioncost = 0.005

    for ticker in portfolio.tickersymbolist:
        if portfolio[ticker].stocks > 0:
            sell = portfolio[ticker].stocks * (portfolio.simulationdf['Price' + ticker][dfindex])
            portfolio[ticker].capital += sell - transactioncost
            portfolio[ticker].stocks = 0

    return portfolio

#always after selling stocks
def allocatecapital(portfolio, weightsdf, dfindex):
    portfolio.availablecapital  = portfolio.getportfoliovalue(dfindex)
    availablecapital = portfolio.availablecapital
    for ticker in portfolio.tickersymbolist:
        portfolio[ticker].capital = availablecapital * float(weightsdf['Weight' + ticker][dfindex])
        portfolio.availablecapital -= portfolio[ticker].capital

    return portfolio

def makeplot(portfolio, weightsdf, portfoliovalue_day, portfoliovalue_month):
    style.use('seaborn-whitegrid')
    fig, ax = plt.subplots()


    # *********** Plot ROR ***********
    pricedatadftesting = portfolio.simulationdf
    valuestockarray = [i / portfolio.initialcapital * 100 - 100 for i in portfoliovalue_day]

    ax = plt.subplot2grid((3, 1), (0, 0), colspan=1, rowspan=2)
    ax.xaxis.set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.plot(pricedatadftesting.index.tolist(), valuestockarray, 'b-', label = '% ROR', )
    ax.fmt_xdata = mdates.DateFormatter('%Y-%m')
    ax.set_title('Portfolio Return of:\n'+str(portfolio.tickersymbolist))
    legend = ax.legend(frameon=True, loc='upper left', shadow=True, fontsize='medium')

    # Star point at the end
    ax.plot(pricedatadftesting.index.tolist()[-1], valuestockarray[-1], 'b*', label = '% ROR', )
    label = "{:.2f} %".format(valuestockarray[-1])
    plt.annotate(label, (pricedatadftesting.index.tolist()[-1], valuestockarray[-1]), textcoords="offset points", xytext=(0, 10), ha='center')

    # *********** Bar plot ***********
    returns_series = pd.Series(portfoliovalue_month)
    list_returns = returns_series.pct_change().tolist()
    list_returns[0] = 0
    list_returns = [100 * x for x in list_returns]

    ax = plt.subplot2grid((3, 1), (2, 0), colspan=1, rowspan=1, sharex=ax)
    barlist = ax.bar(weightsdf.index.tolist(), list_returns, label='Monthly Returns (%)', width=20)
    for index_bar in range(len(barlist)):
        if list_returns[index_bar] <= 0:
            barlist[index_bar].set_color('r')
        else:
            barlist[index_bar].set_color('g')

    #for x, y in zip(pricedatadftesting.index.tolist(), list_returns):
    #    label = "{:.2f}".format(y)
    #    if y <= 0:
    #        plt.annotate(label, (x, y), textcoords="offset points", xytext=(0, 2), ha='center', fontsize=8)
    #    else:
    #        plt.annotate(label, (x, y), textcoords="offset points", xytext=(0, 2), ha='center', fontsize=8)

    ax.xaxis.set_visible(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    legend = ax.legend(frameon=True, loc='best', shadow=True, fontsize='medium')

    plt.xticks(rotation=45)
    plt.xlabel('Date')

    #plt.ylim((0,100))
    plt.box(on=None)
    plt.gcf().autofmt_xdate()
    plt.savefig('PNGPortfolio.png')
    plt.legend()
    plt.show()

    return 0

def main(portfolio, weightsdf):

    ntransactions = 0

    portfoliovalue_month = []
    portfoliovalue_day = []
    wi = 0
    for dfindex in portfolio.simulationdf.index:
        # get totalvalue of the portfolio
        totalvalue = portfolio.getportfoliovalue(dfindex)
        portfoliovalue_day.append(totalvalue)

        if dfindex == weightsdf.index[wi]:
            #sell stocks
            sellstocks(portfolio, dfindex)
            #get totalvalue of the portfolio
            totalvalue = portfolio.getportfoliovalue(dfindex)
            portfoliovalue_month.append(totalvalue)
            #allocate capital
            allocatecapital(portfolio, weightsdf, dfindex)
            #buy stocls
            buystocks(portfolio, dfindex)

            #increment wi until last index
            if wi < len(weightsdf.index)-1:
                wi += 1
            else:
                continue

    # working on the plot
    makeplot(portfolio, weightsdf, portfoliovalue_day, portfoliovalue_month)

    print('\nLast Day:')
    print(dfindex)
    print(portfolio)

    return 0