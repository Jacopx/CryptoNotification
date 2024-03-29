#!/usr/bin/python

import urllib.request
import json
from pprint import pprint
from prettytable import PrettyTable
import sqlite3
import sys, os
import getopt
import datetime

x = PrettyTable(["Crypto", "Date", "Amount", "Price", "Value", "Difference"])
y = PrettyTable(["Date", "Crypto", "Value"])

conn = sqlite3.connect(os.path.dirname(os.path.abspath(__file__)) + '/active.db')
c = conn.cursor()

try:
      opts, args = getopt.getopt(sys.argv, "dualp")
except getopt.GetoptError:
      print('Usage: -d Display wallet, -u Update DB, -l Log of market or -a Add buy')
      sys.exit(2)
for arg in args:
    if arg == '-d':
        totAct = 0
        totDiff = 0
        totAmount = 0
        response = urllib.request.urlopen("https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=EUR")
        data = json.loads(response.read().decode('utf8'))

        price_eur = float(data[0]['price_eur'])

        c.execute('SELECT * FROM Trans;')
        all_rows = c.fetchall()
        for row in all_rows:
            act = float(row[3])*price_eur
            diff = act - float(row[4])
            date = datetime.datetime.strptime(row[2], "%d%m%y").strftime("%d-%m-%y")

            totAmount += row[3]
            totAct += act
            totDiff += diff

            x.add_row([row[1], date, row[3], ("%.2f €" % price_eur), ("%.2f €" % act), ("%.2f €" % diff)])

        x.add_row(["---","------", "----------", "------", "------", "------" ])
        x.add_row(["TOTAL", "", totAmount, "", ("%.2f €" % totAct), ("%.2f €" % totDiff)])
        print(x)
    elif arg == '-p':
        response = urllib.request.urlopen("https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=EUR")
        data = json.loads(response.read().decode('utf8'))
        y.add_row([str(datetime.datetime.now()), data[0]['symbol'], float(data[0]['price_eur'])])
        print(y)

    elif arg == '-a':
        sym = input("Insert symbol of Crypto: ")
        num = float(input("Insert amount of %s: " % sym))
        paid = float(input("Insert paid for {0} of {1}: ".format(num, sym)))
        date = input("Insert date of transaction (DDMMYY): ")

        c.execute("INSERT INTO Trans(Type, Date, Amount, Paid) VALUES (?,?,?,?);", (sym, date, num, paid))
        conn.commit()

    elif arg == '-u':
        response = urllib.request.urlopen("https://api.coinmarketcap.com/v1/ticker/bitcoin/?convert=EUR")
        data = json.loads(response.read().decode('utf8'))
        c.execute("INSERT INTO History(TimeStamp, Type, Price) VALUES (?,?,?);", (str(datetime.datetime.now()), data[0]['symbol'], float(data[0]['price_eur'])))
        conn.commit()

    elif arg == '-l':
        c.execute('SELECT * FROM History;')
        all_rows = c.fetchall()
        for row in all_rows:
            y.add_row([row[0], row[1], row[2]])

        print(y)
