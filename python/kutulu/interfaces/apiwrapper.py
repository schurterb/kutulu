"""
@auther schurterb
@date 17-12-8
@description
 Base API wrapper defining the methods which must be implemented by each 
exchange specific api.
"""

import abc

class ExchangeAPIWrapper(metclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def __connect(self):
        pass
       
    @abc.abstractmethod
    def __disconnect(self):
        pass  
    
    """
    Returns the current time on the Exchange Server
    """
    @abc.abstractmethod
    def getExchangeServerTime(self):
        pass
    
    """
    Returns the current account balance of the user
    """
    @abc.abstractmethod
    def getAccountBalance(self):
        pass
    
    """
    Returns exchange data about the given asset pairs
    """
    @abc.abstractmethod
    def getAssetInfo(self, asset_list):
        pass
    
    """
    Returns price data about the given asset pairs
    """
    @abc.abstractmethod
    def pollAssetPrices(self, asset_list):
        pass
    
    """
    Submit a list of orders to the exchange
    """
    @abc.abstractmethod
    def submitOrders(self, orders):
        pass
    
    """
    Returns a list of closed orders placed by the user
    Closed orders my be orders canceled by the user or filled on the exchange
    """
    @abc.abstractmethod
    def listClosedOrders(self):
        pass
    
    """
    Returns a list of open orders placed by the user
    """
    @abc.abstractmethod
    def listOpenOrders(self):
        pass
        
    """
    Returns the order book lists up to a given depth
    """
    @abc.abstractmethod
    def getOrderBooks(self, asset_pairs, depth=20):
        pass
    
    """
    Returns the ask-bid spread starting from a given time
    """
    @abc.abstractmethod
    def getSpreadHistory(self, asset_pairs, start_date=None):
        pass
    
    """
    Returns the most recent trades executed on the exchange
    """
    @abc.abstractmethod
    def getRecentTrades(self, asset_pairs):
        pass
    
    """
    Submits requests to transfer crypto currencies to different exchanges
    """
    @abc.abstractmethod
    def transferCurrency(self, transfer_requests):
        pass
    