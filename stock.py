#!/usr/bin/py

import math
from operator import itemgetter

# A dictionary with k=stock name and v=list of stock prices
stocks = {}

# A dictionary with k=stock name and v=oscillation
stocks_oscillation = {}

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
                stock_prices.append([float(i) for i in temp[1:]])
                stocks[temp[0]] = stock_prices
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
    oscillation = 0.0

    for i in xrange(0, len(prices)):
        if i == 1:
            continue
        change = prices[i] - prices[i-1]
        tmp = change / prices[i-1] 
    oscillation = oscillation + tmp
    
    stocks_oscillation[name] = oscillation

def analyse(money, name, owned):
    global stocks
    global stocks_oscillation

    for n in name:
        price = stocks[n]
        calculate_oscillation(n, price)

    sell_stocks(name, owned)
    select_stocks(money)
    
def sell_stocks(name, owned):
    global stocks_sold
    
    for i in xrange(0, len(name)):
        n = name[i]
        o = owned[i]
        osc = stocks_oscillation[n]
    if osc < 0 and o > 0:
        stocks_sold.append((n,o))

def select_stocks(money):
    global stocks
    global stocks_purchased
    global stocks_oscillation

    proportion = {1:[1.0], 2:[0.7,0.3], 3:[0.5,0.3,0.2], 4:[0.4,0.3,0.2,0.1]}
    sorted_stocks_oscillation = sorted(stocks_oscillation.iteritems(), key = itemgetter(1), reverse=True)
   
    #print "Stock oscillation : {0}".format(sorted_stocks_oscillation)

    purchase_stock = []

    for i in xrange(0, len(sorted_stocks_oscillation)):
        if i > 3:
            break
        name = sorted_stocks_oscillation[i][0]
        osc = sorted_stocks_oscillation[i][1]
        price = stocks[name][-1]
        if osc > 0:
            purchase_stock.append((name,price))
   
    #print "Purchase Stock : {0}".format(purchase_stock)
    no_of_stocks = len(purchase_stock)
    stock_proportion = proportion[no_of_stocks]
   
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
	#print "Stock name : {0} , Stock owned : {1}, Stock prices : {2}".format(stock_name, stock_owned, stock_prices)
        stocks[stock_name] = stock_prices
    analyse(m, name, owned) 
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
