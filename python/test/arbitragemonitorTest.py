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
good_tickers.append(TickerData("kraken", "BTC", "ETH", 0.03456, 3, 0.03445, 0.6))
good_tickers.append(TickerData("kraken", "BTC", "LTC", 0.02214, 0.1234, 0.02108, 42))
good_tickers.append(TickerData("kraken", "LTC", "ETH", 1.3895, 18, 1.1274, 18))
#GDAX tickers
good_tickers.append(TickerData("gdax", "BTC", "ETH", 0.03578, 10, 0.03466, 10))
good_tickers.append(TickerData("gdax", "BTC", "LTC", 0.02214, 10, 0.02108, 10))
good_tickers.append(TickerData("gdax", "LTC", "ETH", 0.3895, 10, 0.1274, 10))
#Bittrex tickers
good_tickers.append(TickerData("bittrex", "BTC", "ETH", 0.03456, 100, 0.03445, 2))
good_tickers.append(TickerData("bittrex", "BTC", "LTC", 0.03389, 0.317, 0.025, 0.256))
good_tickers.append(TickerData("bittrex", "LTC", "ETH", 1.3895, 4242.8, 1.1274, 3786.925))
#Self-exchange asset values (for initialization)
for exchange in exchanges:
    for base in assets:
        good_tickers.append(TickerData(exchange, base, base, 1.0, 1.0, 1.0, 1.0))
        
rvm = RelativeValueMatrix(exchanges, assets)

config = {}
config["network_fee"] = 0.001
config["exchange_fees"] = {"kraken":0.0026, "gdax":0.0, "bittrex":0.0025}

print("Creating ArbitrageMonitor")
monitor = ArbitrageMonitor(config)
if monitor is not None:
    print("PASS")
else:
    print("FAIL")
    
print("Calculating Arbitrage Opportunities")
opportunities = monitor.checkArbitrageOpportunities(rvm)
print(opportunities)

                