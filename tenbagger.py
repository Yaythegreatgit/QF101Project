#Author: Ioannis Ypsilantis
#Description: This is code to implement the ten baggers project. Functions take
#structural and empirical variables as defined by the assignment itself to return
#revelant data, this includes return % on portfolio and counts.


from numpy.core.fromnumeric import std
import pandas as pd
import pandas_datareader as pr
import numpy as np
import datetime
import math
import random
import matplotlib.pyplot as plt
import urllib3
import certifi

https = urllib3.PoolManager( cert_reqs = 'CERT_REQUIRED', ca_certs =certifi.where())
url = https.urlopen('GET','https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
SP500=pd.read_html(url.data)[0]

Russell = pd.read_excel("Russell-2000-Stock-Tickers-List.xlsx")

url = https.urlopen('GET','https://stockmarketmba.com/listofcompaniesthathavemergedwithaspac.php')
SPAC = pd.read_html(url.data)[0]

#helper functions

#Returns a list of random stocks of size sizeof
def generaterandom(sizeof):
    fulllist = pr.nasdaq_trader.get_nasdaq_symbols().loc[:,['NASDAQ Symbol']].values.tolist()
    return random.sample(fulllist, sizeof)
#Returns a list of random stocks of size sizeof from S&P500    
def generaterandomSP(sizeof):
    fulllist = SP500.loc[:,"Symbol"].values.tolist()
    return random.sample(fulllist,sizeof)
    
#Returns a list of random stocks of size sizeof from Russell2000
def generaterandomRussell(sizeof):
    fulllist = Russell.loc[:,"Ticker"].values.tolist()
    return random.sample(fulllist,sizeof)
#Returns a list of random stocks of size sizeof from SPACS
#(I think this could be interesting not sure if you guys want to test this one)
def generaterandomSPAC(sizeof):
    fulllist = SPAC.loc[:,"Symbol"].values.tolist()
    return random.sample(fulllist,sizeof)
#Returns a list of random stocks of size sizeof from given country
def generaterandomCountry(sizeof, country):
    return 0

#structural variables

#Generates a fake portfolio, assuming equal money was invested in each.
#Tenbaggers have return of nobags, so a regular tenbagger should have nobags of 10
#Nontenbaggers have return based on normal distribution.
#Returns the %return with and without ten baggers as pair
def calculateReturnFake(sizeof, no10s, nobags):
    if (sizeof < no10s):
        return "no of Ten Baggers cannot exceed sizeof portfolio"
    tens = np.full((no10s), nobags, dtype=np.double)
    random = np.random.normal(0, 0.3, sizeof-no10s)
    portfolio = np.concatenate((tens, random))
    return np.average(portfolio)
    
    

#Given a portfolio, starttime, and endtime generates pertinent data,
#No. of ten baggers, return on portfolio.
def calculateReturn(portfolio, starttime, endtime):
    return 0

#Empirical variables

#Returns No of 10baggers found in date range starting from starttime and
#lasting for analysis period. Time to hold stocks is window length
#Making windowlength and analysis period equal will keep a static window
def counttenbaggers(starttime, windowlength, analysisperiod):
    return 0
