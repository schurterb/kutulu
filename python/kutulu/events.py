"""
@auther schurterb
@date 17-12-5
@description
 Events used to generalize access to the various exchange APIs. Each API wrapper
 must handle these events and translate them for the exchanges API.
"""

import random

class AssetInfo:
    
    def __init__(self, asset, volume, **kwargs):
        self.asset = asset
        self.volume = volume
        #This is the volume held for various orders and withdraws.
        self.held = float(kwargs.get("held_volume", 0.0))


class TickerInfo: 
    
    def __init__(self, exchange, base, quote, **kwargs):
        self.exchange = exchange
        self.base = base
        self.quote = quote
        self.min_order_size = float(kwargs.get("min_order_size", 0.01))
        self.max_order_size = float(kwargs.get("max_order_size", 1000.00))
        self.order_precision = float(kwargs.get("order_precision", 2))
        #TODO: define all necessary ticker info fields

        
class TickerData:
    
    def __init__(self, exchange, base, quote, ask, bid):
        self.exchange = exchange
        self.base = base
        self.quote = quote
        self.ask = ask
        self.bid = bid
      
      
"""
This is mainly intended for initializing the system with reasonable moving averages
"""
class TickerHistory:
    
    def __init__(self, exchange, base, quote, time_intervals, ask_history, bid_history, **kwargs):
        self.exchange = exchange
        self.base = base
        self.quote = quote
        self.time_intervals = time_intervals
        self.ask_history = ask_history
        self.bid_history = bid_history
        

class OrderBook:
    
    def __init__(self, exchange, base, quote, bids, asks, time, **kwargs):
        self.exchange = exchange
        self.base = base
        self.quote = quote
        self.bids = bids
        self.asks = asks
        self.time = time


class Order:
    
    exchange = None
    base = None
    quote = None
    action = None
    ordertype="limit"
    price = None
    volume = 0
    expiretime = 300 #seconds = the max time the order should remain on the books
    fee_in_base = False 
    success = False
    orderId = random.randint(0, 2147483647)
    

class BuyOrder(Order):
    
    def __init__(self, exchange, base, quote, price, volume, **kwargs):
        self.exchange = exchange
        self.base = base
        self.quote = quote
        self.price = price
        self.volume = volume
        self.expiretime = kwargs.get("expire_time", 300)
        self.action = "buy"
        self.feeFlag = True
            
    
class SellOrder(Order):
    
    def __init__(self, exchange, base, quote, price, volume, **kwargs):
        self.exchange = exchange
        self.base = base
        self.quote = quote
        self.price = price
        self.volume = volume
        self.expiretime = kwargs.get("expire_time", 300)
        self.action = "sell"
        self.feeFlag = False
            
            
class TransferRequest:
    
    def __init__(self, exchange, asset, volume, destination, **kwargs):
        self.exchange = exchange
        self.asset = asset
        self.volume = volume
        self.destination = destination