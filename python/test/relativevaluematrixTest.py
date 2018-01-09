"""
@auther schurterb
@date 17-12-12
@description
 Test script for the RelativeValueMatrix class implementation
"""


import sys
sys.path.append("../kutulu")

from events import *
from engine.relativevaluematrix import RelativeValueMatrix

exchanges = ["kraken", "gdax", "bittrex"]
assets = ["BTC", "ETH", "LTC"]

print("Initializing test")
good_tickers = []
for exchange in exchanges:
    good_tickers.append(TickerData(exchange, "BTC", "ETH", 42.0, 10, 41.0, 20))
    good_tickers.append(TickerData(exchange, "BTC", "LTC", 42.0, 20, 41.0, 10))
    good_tickers.append(TickerData(exchange, "LTC", "ETH", 42.0, 5, 41.0, 5))
    for base in assets:
        good_tickers.append(TickerData(exchange, base, base, 1.0, 1.0, 1.0, 1.0))
bad_name_tickers = []
bad_name_tickers.append(TickerData("nasdaq", "BTC", "LTC", 42.0, 10, 41.0, 10))
bad_name_tickers.append(TickerData(None, "LTC", "ETH", 442.0, 10, 41.0, 10))
bad_name_tickers.append(TickerData("kraken", "COW", "ETH", 42.0, 10, 41.0, 10))
bad_name_tickers.append(TickerData("kraken", None, "LTC", 42.0, 10, 41.0, 10))
bad_name_tickers.append(TickerData("kraken", "BTC", "COW", 42.0, 10, 41.0, 10))
bad_name_tickers.append(TickerData("kraken", "LTC", None, 42.0, 10, 41.0, 10))
bad_value_tickers = []
bad_value_tickers.append(TickerData("kraken", "BTC", "ETH", -10, 10, 1.0/-10, 10))
bad_value_tickers.append(TickerData("kraken", "BTC", "ETH", 0.001, 10, -0.05, 10))
                
                
print("Creating Matrix...")
matrix = RelativeValueMatrix(exchanges, assets)
if type(matrix) is RelativeValueMatrix:
    print("PASS")
else:
    print("FAIL")


print("Updating Matrix with good data...")
matrix.updateRelativeValues(good_tickers)

print("Checking Matrix updates...")
check = True
for ticker in good_tickers:
    if((matrix.getAsk(ticker.exchange, ticker.base, ticker.quote) != ticker.ask) or
       (matrix.getAsk(ticker.exchange, ticker.quote, ticker.base) != 1.0/ticker.bid) or
       (matrix.getBid(ticker.exchange, ticker.base, ticker.quote) != ticker.bid) or
       (matrix.getBid(ticker.exchange, ticker.quote, ticker.base) != 1.0/ticker.ask)):
           print(matrix.getAsk(ticker.exchange, ticker.base, ticker.quote)," != ",ticker.ask)
           print(matrix.getAsk(ticker.exchange, ticker.quote, ticker.base)," != ",1.0/ticker.bid)
           print(matrix.getBid(ticker.exchange, ticker.base, ticker.quote)," != ",ticker.bid)
           print(matrix.getBid(ticker.exchange, ticker.quote, ticker.base)," != ",1.0/ticker.ask)
           check = False
if check:
    print("PASS")
else:
    print("FAIL")
  

print("Updating Matrix with bad data...")
matrix.updateRelativeValues(bad_name_tickers)
matrix.updateRelativeValues(bad_value_tickers)

print("Checking Matrix updates...")
check = True
for ticker in good_tickers:
    if((matrix.getAsk(ticker.exchange, ticker.base, ticker.quote) != ticker.ask) or
       (matrix.getAsk(ticker.exchange, ticker.quote, ticker.base) != 1.0/ticker.bid) or
       (matrix.getBid(ticker.exchange, ticker.base, ticker.quote) != ticker.bid) or
       (matrix.getBid(ticker.exchange, ticker.quote, ticker.base) != 1.0/ticker.ask)):
           print(matrix.getAsk(ticker.exchange, ticker.base, ticker.quote)," != ",ticker.ask)
           print(matrix.getAsk(ticker.exchange, ticker.quote, ticker.base)," != ",1.0/ticker.bid)
           print(matrix.getBid(ticker.exchange, ticker.base, ticker.quote)," != ",ticker.bid)
           print(matrix.getBid(ticker.exchange, ticker.quote, ticker.base)," != ",1.0/ticker.ask)
           check = False
for ticker in bad_name_tickers:
    if((matrix.getAsk(ticker.exchange, ticker.base, ticker.quote) != None) or
       (matrix.getAsk(ticker.exchange, ticker.quote, ticker.base) != None) or
       (matrix.getBid(ticker.exchange, ticker.base, ticker.quote) != None) or
       (matrix.getBid(ticker.exchange, ticker.quote, ticker.base) != None)):
           print(matrix.getAsk(ticker.exchange, ticker.base, ticker.quote)," != ",ticker.ask)
           print(matrix.getAsk(ticker.exchange, ticker.quote, ticker.base)," != ",1.0/ticker.bid)
           print(matrix.getBid(ticker.exchange, ticker.base, ticker.quote)," != ",ticker.bid)
           print(matrix.getBid(ticker.exchange, ticker.quote, ticker.base)," != ",1.0/ticker.ask)
           check = False
           
for ticker in bad_value_tickers:
    if((matrix.getAsk(ticker.exchange, ticker.base, ticker.quote) == ticker.ask) or
       (matrix.getAsk(ticker.exchange, ticker.quote, ticker.base) == 1.0/ticker.bid) or
       (matrix.getBid(ticker.exchange, ticker.base, ticker.quote) == ticker.bid) or
       (matrix.getBid(ticker.exchange, ticker.quote, ticker.base) == 1.0/ticker.ask)):
           print(matrix.getAsk(ticker.exchange, ticker.base, ticker.quote)," != ",ticker.ask)
           print(matrix.getAsk(ticker.exchange, ticker.quote, ticker.base)," != ",1.0/ticker.bid)
           print(matrix.getBid(ticker.exchange, ticker.base, ticker.quote)," != ",ticker.bid)
           print(matrix.getBid(ticker.exchange, ticker.quote, ticker.base)," != ",1.0/ticker.ask)
           check = False
if check:
    print("PASS")
else:
    print("FAIL")
    
#  "{0:0.6f}".format(usd_profit_loss[1]).ljust(13)
    
print("Checking rvm calculations")
for exchange in exchanges:
    print("## echange = ",exchange)
    print(" base : quote : average : spread : weighted average : weighted spread ")
    for base in assets:
        for quote in assets:
            avg = matrix.getAverage(exchange, base, quote)
            spd = matrix.getSpread(exchange, base, quote)
            w_avg = matrix.getWeightedAverage(exchange, base, quote)
            w_spd = matrix.getWeightedSpread(exchange, base, quote)
            if avg is not None:
                avg = "{0:0.4f}".format(float(avg)).ljust(7)
            if spd is not None:
                spd = "{0:0.4f}".format(float(spd)).ljust(6)
            if w_avg is not None:
                w_avg = "{0:0.4f}".format(float(w_avg)).ljust(16)
            if w_spd is not None:
                w_spd = "{0:0.4f}".format(float(w_spd)).ljust(15)
            msg = " "+str(base)+" : "+str(quote)+"  : "+str(avg)+" : "+str(spd)+" : "+str(w_avg)+" : "+str(w_spd)
            print(msg)
#            
#print("Checking spreads...")
#for exchange in exchanges:
#    print("## echange = ",exchange)
#    for base in assets:
#        for quote in assets:
#            val = matrix.getSpread(exchange, base, quote)
#            print(base,":",quote,":",val)
#            
#print("Checking weighted average values...")
#for exchange in exchanges:
#    print("## echange = ",exchange)
#    for base in assets:
#        for quote in assets:
#            val = matrix.getWeightedAverage(exchange, base, quote)
#            print(base,":",quote,":",val)
#            
#print("Checking weighted spreads...")
#for exchange in exchanges:
#    print("## echange = ",exchange)
#    for base in assets:
#        for quote in assets:
#            val = matrix.getSpread(exchange, base, quote)
#            print(base,":",quote,":",val)