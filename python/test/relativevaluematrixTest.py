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
    good_tickers.append(TickerData(exchange, "BTC", "ETH", 42.0, 1.0/42.0))
    good_tickers.append(TickerData(exchange, "BTC", "LTC", 42.0, 1.0/42.0))
    good_tickers.append(TickerData(exchange, "LTC", "ETH", 42.0, 1.0/42.0))
    for base in assets:
        good_tickers.append(TickerData(exchange, base, base, 1.0, 1.0))
bad_tickers = []
bad_tickers.append(TickerData("nasdaq", "BTC", "LTC", 42.0, 1.0/42.0))
bad_tickers.append(TickerData(None, "LTC", "ETH", 42.0, 1.0/42.0))
bad_tickers.append(TickerData("kraken", "COW", "ETH", 42.0, 1.0/42.0))
bad_tickers.append(TickerData("kraken", None, "LTC", 42.0, 1.0/42.0))
bad_tickers.append(TickerData("kraken", "BTC", "COW", 42.0, 1.0/42.0))
bad_tickers.append(TickerData("kraken", "LTC", None, 42.0, 1.0/42.0))
bad_tickers.append(TickerData("kraken", "BTC", "ETH", -10, 1.0/-10))
bad_tickers.append(TickerData("kraken", "BTC", "ETH", 0.0, 0.0))
                
                
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
       (matrix.getAsk(ticker.exchange, ticker.quote, ticker.base) != 1.0/ticker.ask) or
       (matrix.getBid(ticker.exchange, ticker.base, ticker.quote) != ticker.bid) or
       (matrix.getBid(ticker.exchange, ticker.quote, ticker.base) != 1.0/ticker.bid)):
           print(matrix.getAsk(ticker.exchange, ticker.base, ticker.quote)," != ",ticker.ask)
           print(matrix.getAsk(ticker.exchange, ticker.quote, ticker.base)," != ",1.0/ticker.ask)
           print(matrix.getBid(ticker.exchange, ticker.base, ticker.quote)," != ",ticker.bid)
           print(matrix.getBid(ticker.exchange, ticker.quote, ticker.base)," != ",1.0/ticker.bid)
           check = False
if check:
    print("PASS")
else:
    print("FAIL")
  

print("Updating Matrix with bad data...")
matrix.updateRelativeValues(bad_tickers)

print("Checking Matrix updates...")
check = True
for ticker in good_tickers:
    if((matrix.getAsk(ticker.exchange, ticker.base, ticker.quote) != ticker.ask) or
       (matrix.getAsk(ticker.exchange, ticker.quote, ticker.base) != 1.0/ticker.ask) or
       (matrix.getBid(ticker.exchange, ticker.base, ticker.quote) != ticker.bid) or
       (matrix.getBid(ticker.exchange, ticker.quote, ticker.base) != 1.0/ticker.bid)):
           print(matrix.getAsk(ticker.exchange, ticker.base, ticker.quote)," != ",ticker.ask)
           print(matrix.getAsk(ticker.exchange, ticker.quote, ticker.base)," != ",1.0/ticker.ask)
           print(matrix.getBid(ticker.exchange, ticker.base, ticker.quote)," != ",ticker.bid)
           print(matrix.getBid(ticker.exchange, ticker.quote, ticker.base)," != ",1.0/ticker.bid)
           check = False
for ticker in bad_tickers:
    if((matrix.getAsk(ticker.exchange, ticker.base, ticker.quote) != None) or
       (matrix.getAsk(ticker.exchange, ticker.quote, ticker.base) != None) or
       (matrix.getBid(ticker.exchange, ticker.base, ticker.quote) != None) or
       (matrix.getBid(ticker.exchange, ticker.quote, ticker.base) != None)):
           print(matrix.getAsk(ticker.exchange, ticker.base, ticker.quote)," != ",ticker.ask)
           print(matrix.getAsk(ticker.exchange, ticker.quote, ticker.base)," != ",1.0/ticker.ask)
           print(matrix.getBid(ticker.exchange, ticker.base, ticker.quote)," != ",ticker.bid)
           print(matrix.getBid(ticker.exchange, ticker.quote, ticker.base)," != ",1.0/ticker.bid)
           check = False
if check:
    print("PASS")
else:
    print("FAIL")