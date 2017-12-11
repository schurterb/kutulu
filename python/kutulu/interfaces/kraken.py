"""
@auther schurterb
@date 17-12-11
@description
 Kraken exchange API wrapper
"""

from apiwrapper import ExchangeAPIWrapper

class KrakenAPI(ExchangeAPIWrapper):
    
    def __init__(self, config, **kwargs):
        pass
    
    def __del__(self):
        pass
    
    def __connect(self):
        pass
       
    def __disconnect(self):
        pass  
    
    """
    Returns the current time on the Exchange Server
    """
    def getExchangeServerTime(self):
        pass
    
    """
    Returns the current account balance of the user
    """
    def getAccountBalance(self):
        pass
    
    """
    Returns exchange data about the given asset pairs
    """
    def getAssetInfo(self, asset_list):
        pass
    
    """
    Returns price data about the given asset pairs
    """
    def pollAssetPrices(self, asset_list):
        pass
    
    """
    Submit a list of orders to the exchange
    """
    def submitOrders(self, orders):
        pass
    
    """
    Returns a list of closed orders placed by the user
    Closed orders my be orders canceled by the user or filled on the exchange
    """
    def listClosedOrders(self):
        pass
    
    """
    Returns a list of open orders placed by the user
    """
    def listOpenOrders(self):
        pass
        
    """
    Returns the order book lists up to a given depth
    """
    def getOrderBooks(self, asset_pairs, depth=20):
        pass
    
    """
    Returns the ask-bid spread starting from a given time
    """
    def getSpreadHistory(self, asset_pairs, start_date=None):
        pass
    
    """
    Returns the most recent trades executed on the exchange
    """
    def getRecentTrades(self, asset_pairs):
        pass
    