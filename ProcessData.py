import pandas as pd
import numpy as np
from sys import exit
import math
import time
import os.path


# get next day allocation day
def nextallocationday_month(pricedatadf, allocationday, fixedday):

    trainindex = allocationday
    countmonth = allocationday.month
    countyear = allocationday.year

    countmonth += 1
    if countmonth == 13:
        countyear += 1
        countmonth = 1

    trainindex = trainindex.replace(year=countyear, month=countmonth, day=fixedday)
    if pricedatadf[trainindex:].empty:
        nextallocday = 'Out'
    else:
        nextallocday = pricedatadf[trainindex:].index[0]

    return nextallocday

# get DataFrame with price returns
# One Day per Month During one Year (example: fist day of each month)
def getslicedreturns_month(pricedatadf, allocationday, fixedday):

    trainindex = allocationday
    # get date index from 1 YEAR AGO
    trainindex = trainindex.replace(year=trainindex.year-1, day=fixedday)
    sliceindex = pricedatadf[trainindex:allocationday].index[0]

    countyear = trainindex.year
    countmonth = allocationday.month
    sliceddataframe = pd.DataFrame(columns=list(pricedatadf))
    for index in pricedatadf[sliceindex:allocationday].index:
        difference = index - sliceindex

        if difference.days == 0:
            sliceddataframe = pd.concat([sliceddataframe, pricedatadf.loc[[index]]], axis=0)

            countmonth += 1
            if countmonth == 13:
                countyear += 1
                countmonth = 1

            sliceindex = sliceindex.replace(year=countyear, month=countmonth, day=fixedday)
            if sliceindex > pricedatadf.index[-1]:
                break

            sliceindex = pricedatadf[sliceindex:].index[0]

    returnsdf = sliceddataframe.pct_change(1)

    return returnsdf

# get DataFrame with price returns
# All Days full Year
def getdailyreturns_year(pricedatadf, allocationday, fixedday):

    trainindex = allocationday
    trainindex = trainindex.replace(year=trainindex.year-1, day=fixedday)

    sliceddataframe = pd.DataFrame(columns=list(pricedatadf))
    sliceddataframe = pricedatadf[trainindex:allocationday]

    returnsdf = sliceddataframe.pct_change(1)

    return returnsdf

# get DataFrame with price returns
# All Days full Month
def getdailyreturns_month(pricedatadf, allocationday, fixedday):

    trainindex = allocationday
    thismonth = trainindex.month
    thisyear = trainindex.year
    if thismonth == 1:
        lastmonth = 12
        lastyear = thisyear-1
    else:
        lastmonth = thismonth-1
        lastyear = thisyear

    trainindex = trainindex.replace(year = lastyear, month=lastmonth, day=fixedday)

    sliceddataframe = pd.DataFrame(columns=list(pricedatadf))
    sliceddataframe = pricedatadf[trainindex:allocationday]

    returnsdf = sliceddataframe.pct_change(1)

    return returnsdf
