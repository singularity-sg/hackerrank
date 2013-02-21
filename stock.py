#!/usr/bin/py

import math
from operator import itemgetter

# A dictionary with k=stock name and v=list of stock prices
stocks = {}

# A dictionary with k=stock name and v=oscillation
stocks_oscillation = {}

# A dictionary with k=stock name and v=difference with median price
stocks_median = {}

# Stocks to purchase
stocks_purchased = [] 

# Stocks to sell
stocks_sold = []

def readData():
    global stocks
    try:
        with open('stock.txt','r+') as stocks_file:
            for line in stocks_file:
                stock_prices = [] 
                temp = line.split() 
                stock_prices = [float(i) for i in temp[1:]]
                stocks[temp[0]] = stock_prices
        #print "Stocks after reading : {0}".format(stocks)
    except EnvironmentError:
        f = open('stock.txt','w+')

        
def writeData():
    global stocks
    try:
        with open('stock.txt','w+') as stocks_file:
            for stock,prices in stocks.iteritems():
                stocks_file.write(stock + ' ')
                for price in prices:
                    stocks_file.write(str(price) + ' ')
                stocks_file.write('\n')
    except EnvironmentError:
        f = open('stock.txt')

def calculate_oscillation(name, prices):
    global stocks_oscillation
    window = 5 
    acceleration = 0.0
    price_len = len(prices)
   
    if len(prices) < window:
        stocks_oscillation[name] = acceleration
        return
    
    smoothed_prices = []
    no_of_windows = int(math.floor(price_len / window))

    for i in xrange(0, price_len):
        window_sum = 0.0
        window_avg = 0.0
        if (i+window-1) > price_len:
            for j in xrange(i,price_len):
                window_sum = window_sum + prices[j]
            window_avg = window_sum / (price_len - i)
        else:
            for j in xrange(i, i+window-1):
                window_sum = window_sum + prices[j]
            window_avg = window_sum / window
            
        smoothed_prices.append(window_avg)
    
    print "Smoothed Prices: {0}".format(smoothed_prices)

    if len(smoothed_prices) > 1:
        change = smoothed_prices[-1] - smoothed_prices[-2]
        if smoothed_prices[-2] > 0:
            acceleration = change / smoothed_prices[-2]
            
    stocks_oscillation[name] = acceleration

def calculate_median(name, prices):
    global stocks_median
    sorted_prices = sorted(prices)
    median = int(math.floor(len(sorted_prices) / 2))
    median_price = sorted_prices[median]
    change = prices[-1] - median_price
    stocks_median[name] = (change / median_price)

def analyse(money, name, owned, days_left):
    global stocks
    global stocks_oscillation

    for n in name:
        price = stocks[n]
        calculate_oscillation(n, price)
        calculate_median(n, price)
    
    #print "Stock oscillation : {0}".format(stocks_oscillation)
    #print "Stock median : {0}".format(stocks_median)
    sell_stocks(name, owned, (days_left==1))
    select_stocks(money, days_left)
    
def sell_stocks(name, owned, last_day):
    global stocks_sold
   
    for i in xrange(0, len(name)):
        n = name[i]
        o = owned[i]
        osc = stocks_oscillation[n]
        median = stocks_median[n]

        if (last_day):
            if o > 0:
                stocks_sold.append((n,o))
        elif osc < 0.2  and o > 0 and median > 0:
            stocks_sold.append((n,o))

def select_stocks(money, days_left):
    global stocks
    global stocks_purchased
    global stocks_oscillation
    global stocks_median

    #sorted_stocks_oscillation = sorted(stocks_oscillation.iteritems(), key = itemgetter(1), reverse=True)
    sorted_stocks_median = sorted(stocks_median.iteritems(), key = itemgetter(1), reverse=False)
   
    purchase_stock = []

    for i in xrange(0, len(sorted_stocks_median)):
        name = sorted_stocks_median[i][0]
        median = stocks_median[name]
        osc = stocks_oscillation[name]
        price = stocks[name][-1]
        if osc > 0.2 and median < -0.4 and days_left > 10:
            purchase_stock.append((name,price))
   
    #print "Purchase Stock : {0}".format(purchase_stock)
    no_of_stocks = len(purchase_stock)
    
    if no_of_stocks == 0:
        return
    
    money_left = money
    for i in xrange(0, no_of_stocks):
        stock_name = purchase_stock[i][0]
        price = purchase_stock[i][1]
        
	if price > money_left:
            continue

        no_of_stocks_invest = math.floor(money_left / price)
	if no_of_stocks_invest > 0:
            stocks_purchased.append((stock_name, no_of_stocks_invest))
	    money_left = money_left - (no_of_stocks_invest * price)

def printTransaction():
    global stocks_purchased
    global stocks_sold

    k = len(stocks_purchased) + len(stocks_sold)

    print k
    #print "Stock purchased : {0}".format(stocks_purchased)
    #print "Stock sold : {0}".format(stocks_sold)
    
    for stock in stocks_purchased:
        print stock[0] + ' BUY ' + str(stock[1])
    
    for stock in stocks_sold:
        print stock[0] + ' SELL ' + str(stock[1])

# Head ends here

# m = Money available
# k = Number of stocks available
# d = Number of days left
# name = Stock name
# owned = Number of stock owned
# prices = Last 5 day's stock price
def process(m, k, d, name, owned, prices):
    global stocks
    global candidates 
    readData()
    for i in xrange(0, k):
        stock_name = name[i]
        stock_owned = owned[i]
        stock_prices = prices[i]
        if stock_name in stocks and len(stocks[stock_name]) > 0:
            stocks[stock_name].append(stock_prices[-1])
        else:
            stocks[stock_name] = stock_prices
        #print "Stock name : {0} , Stock owned : {1}, Stock prices : {2}".format(stock_name, stock_owned, stock_prices)
    analyse(m, name, owned, d) 
    writeData()

# Tail starts here
if __name__ == '__main__':
    m, k, d = [float(i) for i in raw_input().strip().split()]
    k = int(k)
    d = int(d)
    names = []
    owned = []
    prices = []
    for data in range(k):
        temp = raw_input().strip().split()
        names.append(temp[0])
        owned.append(int(temp[1]))
        prices.append([float(i) for i in temp[2:7]])

    process(m, k, d, names, owned, prices)

    printTransaction()

