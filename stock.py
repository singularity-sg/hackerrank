#!/usr/bin/py

# Head ends here

# m = Money available
# k = Number of stocks available
# d = Number of days left
def printTransactions(m, k, d, name, owned, prices):
    print ""

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

    printTransactions(m, k, d, names, owned, prices)
    	
