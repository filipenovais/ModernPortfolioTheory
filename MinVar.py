import ProcessData
import PortfolioClass
import pandas as pd
from scipy.optimize import minimize
import numpy as np
from sys import exit
import math
import time
from matplotlib import pyplot as plt
import os

np.random.seed(12)

def minimizefunction(covariance, expectedreturns):

    # Objective function
    def objective(weights):
        std = getstd(weights, covariance)
        #sharpe = getstd(weights, covariance, expectedreturns)
        return std
    # Constraint function
    def constraint1(weights):
        sumw = 1.0
        for w in np.nditer(weights):
            sumw -= w
        return sumw

    # initiate weight array
    w0 = []
    for i in range(len(expectedreturns)):
        w0.append(0.01)
    w0 = np.asarray(w0)

    # Min and Max value of each weight(w) - percentage of all capital for each Ticker
    b = (0.00, 0.50)
    bnds = (b,) * len(expectedreturns)
    con1 = {'type': 'eq', 'fun': constraint1}
    cons = con1
    sol = minimize(objective, w0, method='SLSQP', bounds=bnds, constraints=cons)

    return sol.x

# get covariance matrix and expected returnsdf
def getcovexpect(returnsdf):

    # expected returnsdf as mean of all returnsdf - 'numpy.ndarray'
    expectedreturns = []
    col_names = list(returnsdf.columns.values)
    for stockprice in col_names:
        expectedreturns.append(returnsdf[stockprice].mean())
    expectedreturns = np.array(expectedreturns)

    print('returnsdf DataFrame')
    print(returnsdf)
    # covariance matrix - 'numpy.ndarray'
    covariance = returnsdf.cov().values

    return covariance, expectedreturns

# get Standard Deviation
def getstd(weights, covariance):

    pvariance = np.dot(weights, np.dot(covariance, weights.transpose()))
    std = math.sqrt(pvariance)

    return std

# get index and save weightsdf to csv
def getweightsdf(weightsdf, weightsdfindex):
    if not os.path.exists('wcsv/'):
        os.makedirs('wcsv/')

    weightsdf.index = weightsdfindex
    weightsdf100 = weightsdf.copy(deep='all')
    weightsdf100[weightsdf100.select_dtypes(include=['number']).columns] *= 100
    print('Weights DataFrame (%)')
    print(weightsdf100.to_string())
    weightsdf.to_csv('wcsv/MinVar.csv')

    return weightsdf


def main(portfolio):

    pricedatadf = portfolio.pricedatadf
    fixedday = pd.to_datetime(portfolio.inputdate_init).day

    # Init wheights Dataframe and datetime index (weightsdfindex)
    column_names = ['Weight' + x  for x in portfolio.tickersymbolist]
    weightsdf = pd.DataFrame(columns=column_names)
    weightsdfindex = []

    # first allocation day
    nextallocday = portfolio.pricedatadf[portfolio.inputdate_init:].index[0]
    i = 0
    while nextallocday != 'Out':
        print('++++++++++++++++++++++++++++++++++++++++')


        # get DataFrame with price returns
        # All Days full Year
        #returnsdf = ProcessData.getdailyreturns_year(pricedatadf, nextallocday, fixedday)
        # All Days full Month
        #returnsdf = ProcessData.getdailyreturns_month(pricedatadf, nextallocday, fixedday)
        # One Day per Month During one Year (example: fist day of each month)
        returnsdf = ProcessData.getslicedreturns_month(pricedatadf, nextallocday, fixedday)

        # get next day allocation day
        nextallocday = ProcessData.nextallocationday_month(pricedatadf, nextallocday, fixedday)

        # get covariance matrix and expected returnsdf
        covariance, expectedreturns = getcovexpect(returnsdf)
        # minimize
        weights = minimizefunction(covariance, expectedreturns)

        # get Standard Deviation
        std = getstd(weights, covariance)

        # save date index in wheighs DataFrame
        weightsdfindex.append(returnsdf.index[-1])
        weightsdf.loc[i] = weights
        i += 1

        print('Expected returnsdf:\t' + str(expectedreturns))
        print('Weigths:         \t' + str(weights*100))
        print('Standard Deviation:\t' + str(std))
        print('Next Alloc Day:  \t' + str(nextallocday))
        print()

    # get index and save weightsdf to csv
    weightsdf = getweightsdf(weightsdf, weightsdfindex)

    return weightsdf

