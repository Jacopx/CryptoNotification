import urllib.request
import json
from pprint import pprint
from prettytable import PrettyTable
import sqlite3
import sys

x = PrettyTable(["Crypto", "Amount", "Price", "Value", "Difference"])

conn = sqlite3.connect('wallet.db')
c = conn.cursor()

if(len(sys.argv) == 1):
    data = json.load(urllib.request.urlopen("https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=EUR"))
    price_eur = float(data[0]['price_eur'])

    c.execute('SELECT * FROM Trans')
    all_rows = c.fetchall()
    for row in all_rows:
        act = float(row[2])*price_eur
        diff = act - float(row[3])
        x.add_row([row[1], row[2], ("%.2f €" % price_eur), ("%.2f €" % act), ("%.2f €" % diff)])

    print(x)

elif(len(sys.argv) == 2):
    sym = input("Insert symbol of Crypto: ")
    num = float(input("Insert amount of %s: " % sym))
    paid = float(input("Insert paid for {0} of {1}: ".format(num, sym)))

    c.execute("INSERT INTO Trans(Type, Amount, Paid) VALUES (?,?,?)", (sym, num, paid))
    conn.commit()
