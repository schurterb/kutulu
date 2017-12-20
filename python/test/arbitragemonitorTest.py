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
from engine.arbitragemonitor import ArbitrageMonitor

exchanges = ["kraken", "gdax", "bittrex"]
assets = ["BTC", "ETH", "LTC"]

print("Initializing test")
good_tickers = []
#Kraken tickers
good_tickers.append(TickerData("kraken", "BTC", "ETH", 0.03456, 0.03445))
good_tickers.append(TickerData("kraken", "BTC", "LTC", 0.02214, 0.02108))
good_tickers.append(TickerData("kraken", "LTC", "ETH", 1.3895, 1.1274))
#GDAX tickers
good_tickers.append(TickerData("gdax", "BTC", "ETH", 0.03578, 0.03466))
good_tickers.append(TickerData("gdax", "BTC", "LTC", 0.02214, 0.02108))
good_tickers.append(TickerData("gdax", "LTC", "ETH", 0.3895, 0.1274))
#Bittrex tickers
good_tickers.append(TickerData("bittrex", "BTC", "ETH", 0.03456, 0.03445))
good_tickers.append(TickerData("bittrex", "BTC", "LTC", 0.03389, 0.025))
good_tickers.append(TickerData("bittrex", "LTC", "ETH", 1.3895, 1.1274))
#Self-exchange asset values (for initialization)
for exchange in exchanges:
    for base in assets:
        good_tickers.append(TickerData(exchange, base, base, 1.0, 1.0))
        
rvm = RelativeValueMatrix(exchanges, assets)

config = {}
config["network_fees"] = 0.00007
config["exchange_fees"] = 0.0026

print("Creating ArbitrageMonitor")
monitor = ArbitrageMonitor(config)
if monitor is not None:
    print("PASS")
else:
    print("FAIL")
    
print("Calculating Arbitrage Opportunities")
opportunities = ArbitrageMonitor.checkArbitrageOpportunities(good_tickers)
print(opportunities)

                