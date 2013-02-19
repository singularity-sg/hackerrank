#!/usr/bin/py

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

def writeData():
    global stocks
    try:
        with open('stock.txt','w') as stocks_file:
        for stock,prices in stocks.iteritems():
            stocks_file.write(stock + ' ')
            for price in prices:
                stocks_file.write(price + ' ')
            stocks_file.write('\n')
    except EnvironmentError:

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
        prices = stocks[n]
        calculate_oscillation(n, prices)

    sell_stocks(name, owned)
    select_stocks(money)
    
def sell_stocks(name, owned):
    global stocks_sold
    
    for i in xrange(0, len(name)):
        n = name[i]
        o = owned[i]
        osc = stocks_oscillation[n]
    if osc < 0:
            stocks_sold.append((n,o))

def select_stocks(money):
    global stocks
    global stocks_purchased
    global stocks_oscillation

    proportion = {1:[1.0], 2:[0.7,0.3], 3:[0.5,0.3,0.2], 4:[0.4,0.3,0.2,0.1]}
    sorted_stocks_oscillation = sorted(stocks_oscillation.iteritems(), key = operator.itemgetter(1), reverse=True)
    
    purchase_stock = []

    for i in xrange(0, len(sorted_stocks_oscillation)):
        if i > 4:
            break
        name = sorted_stocks_oscillation[i][0]
        osc = sorted_stocks_oscillation[i][1]
        price = stocks[name][-1]
    if osc > 0:
        purchase_stock.append((name,price))
    
    no_of_stocks = len(purchase_stock)
    stock_proportion = proportion[no_of_stocks]
    
    for i in xrange(0, no_of_stocks):
        stock_name = purchase_stock[i][0]
        price = purchase_stock[i][1]
        invest_amt = money * stock_proportion[i]
        no_of_stocks_invest = math.floor(invest_amt / price)
        stocks_purchased.append((stock_name, no_of_stocks_invest))

def printTransaction():
    global stocks_purchased
    global stocks_sold

    k = len(stocks_purchased) + len(stocks_sold)

    print k
    
    for stock in stocks_purchased:
        print stock[0] + ' BUY ' + stock[1]
    
    for stock in stocks_sold:
        print stock[0] + ' SELL ' + stock[1]

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
        if stock_name in stocks:
            stocks[stock_name].append(prices[i][-1])
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
