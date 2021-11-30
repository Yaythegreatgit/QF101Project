#Author: Cavin Gada, Yashvardhin Sharma, Pranav Yalamala, Ioannis Ypsilantis
#Description: This is code to implement the ten baggers project. Functions take
#structural and empirical variables as defined by the assignment itself to return
#revelant data, this includes return % on portfolio and counts.


import pandas as pd
import pandas_datareader as pr
import numpy as np
import datetime
import random
import matplotlib.pyplot as plt
import urllib3
import certifi

https = urllib3.PoolManager( cert_reqs = 'CERT_REQUIRED', ca_certs =certifi.where())
url = https.urlopen('GET','https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
SP500=pd.read_html(url.data)[0] #Gets all tables from wikipedia page

Russell = pd.read_excel("Russell-2000-Stock-Tickers-List.xlsx")

url = https.urlopen('GET','https://stockmarketmba.com/listofcompaniesthathavemergedwithaspac.php')
SPAC = pd.read_html(url.data)[0]

#helper functions

#Returns a list of random equities of size sizeof
def generaterandom(sizeof,index):
    if index == "Nasdaq":
        return generaterandomNasdaq(sizeof)
    if index == "SP":
        return generaterandomSP(sizeof)
    if index == "SPAC":
        return generaterandomSPAC(sizeof)
    if index == "Russell":
        return generaterandomRussell(sizeof)
    return "Invalid index: use Nasdaq, SP, or SPAC"


def generaterandomNasdaq(sizeof):
    fulllist = pr.nasdaq_trader.get_nasdaq_symbols().loc[:,['NASDAQ Symbol']].values.tolist()
    return random.sample(fulllist, sizeof)

#Returns a list of random equities of size sizeof from S&P500
def generaterandomSP(sizeof):
    fulllist = SP500.loc[:,"Symbol"].values.tolist()
    return random.sample(fulllist,sizeof)

#Returns a list of random equities of size sizeof from Russell2000
def generaterandomRussell(sizeof):
    fulllist = Russell.loc[:,"Ticker"].values.tolist()
    return random.sample(fulllist,sizeof)

#Returns a list of random equities of size sizeof from SPACS
#(I think this could be interesting not sure if you guys want to test this one)
def generaterandomSPAC(sizeof):
    fulllist = SPAC.loc[:,"Symbol"].values.tolist()
    return random.sample(fulllist,sizeof)

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



#Given a portfolio with # equities, starttime, and endtime generates pertinent data,
#No. of ten baggers, return on portfolio.

#Empirical variables

#Returns list of ten baggers in given portfolio
#Returns should be a dictionary of Ticker : Return
def returntenbaggers(returns):
    tenbaggers = {}
    for stock, number in returns.items():
        if (number >= 10):
            tenbaggers[stock] = number

    return tenbaggers

#Returns an average of the Returns on a dictionary of Ten Baggers
def numberOfBags(tenBaggers):
    if len(tenBaggers) == 0:
        return 0
    else:
        return np.mean(list(tenBaggers.values()))




#Given a portfolio with # equities, starttime, and endtime generates pertinent data,
#No. of ten baggers, return on portfolio.
#Returns individuals returns on
def calculateReturn(portfolio, starttime, endtime):

    # Dictionary of stock tickers to their corresponding returns (decimal)
    returns = {}

    for stock in portfolio:
        try:
            stock_df = pr.DataReader([stock], 'yahoo', starttime, endtime)
            # read the first and last closing price of stock from start-end date (buying and selling)
            sell_price = stock_df[("Close", stock)][-1]
            buy_price = stock_df[("Close", stock)][0]
            # calculate the stock profit (sell - buy)
            stock_return = (sell_price - buy_price)/buy_price

            # update dictionary of returns
            returns[stock] = stock_return

        except:
            print("Error occurred reading " + str(stock) + " Skipping...")
    return returns

# SET UP FOR PORTFOLIO AND  TIMES.
start = datetime.datetime(2019, 1, 1)
end = datetime.datetime(2021, 10, 20)

#Random sample of iterations, using index over time period from start to end
#size range of portfolio supported
def runTests(iter, index, start, end):
    #portfolio exports a dataframe of the following:
    #portfolio (with $1000 investment in each equity)
    #size
    #number of 10 baggers
    #Avg number of bags
    #total return of portfolio
    sizes = []
    no_bags = []
    no_tenbaggers = []
    averages = []
    for i in range(iter):
        n = random.randrange(20, 50) #size of the portfolio is random number from 20 to 50 stocks
        Returns = calculateReturn(generaterandom(n, index), start, end)
        sizes += [len(Returns)]
        tenbaggers = returntenbaggers(Returns)
        no_bags += [numberOfBags(tenbaggers)]
        no_tenbaggers += [len(tenbaggers)]
        averages += [sum(Returns.values())/n]
        print(i)
    return pd.DataFrame({'Size':sizes, 'Number of 10 Baggers':no_tenbaggers, 'Number of Bags':no_bags, 'Actual Return':averages})

#Generating graphs for fake portfolio
def fakeprintgraphs():
    varY = np.zeros((100))
    for i in range(1,101):
        varY[i-1] = calculateReturnFake(i, 1, 10)
    plt.title("Portfolio Size impact on Return")
    plt.plot(varY)
    plt.show()

    varZ = np.zeros((100))
    for i in range(1,101):
        varZ[i-1] = calculateReturnFake(100, i, 10)
    plt.title("Number of Tenbaggers vs Return")
    plt.plot(varZ)
    plt.show()

    varA = np.zeros((100))
    for i in range(1,101):
        varA[i-1] = calculateReturnFake(100, 10, i)
    plt.title("Number of Bags vs Return")
    plt.plot(varA)
    plt.show()

    varB = []
    varC = []
    for i in range(1, 101):
        for j in range(i,101):
            for k in range(1,101):
                varB += [calculateReturnFake(j,i,k)]
                varC += [(i * k)/j]
    plt.title("Equation vs 'Actual'")
    plt.plot(varB, varC)
    plt.show()

#Run testdata
#result = runTests(10, "Russell", start, end)
#Export to excel for expert analysis
#result.to_excel(r'C:\Users\yiann\github\QF101Project\results.xlsx', index = False)

#Generating a specific profile
#stocks = ["AMZN", "NVDA", "WMT", "HSY", "ETSY", "CMCSA", "DIS", "KR", "HAS", "MAT"]
#starti = datetime.datetime(2016, 1, 1)
#endi = datetime.datetime(2021, 10, 20)
#Returns = calculateReturn(stocks, starti, endi)
#tenbaggers = returntenbaggers(Returns)
#no_bags = numberOfBags(tenbaggers)
#no_tenbaggers = len(tenbaggers)
#averages = sum(Returns.values())/10
