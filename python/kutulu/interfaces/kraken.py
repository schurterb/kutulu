"""
@auther schurterb
@date 17-12-11
@description
 Kraken exchange API wrapper
"""

import sys
sys.path.append("..")

from apiwrapper import ExchangeAPIWrapper
from logger import Logger
from events import *

import krakenex
import traceback
import time

class KrakenAPI(ExchangeAPIWrapper):
    
    def __init__(self, keys, spread_percentages, **kwargs):
        self.log = Logger("interface","KrakenAPI","DEBUG")
        self.testmode = kwargs.get("testmode",False)
        self.spread_percentage = spread_percentages
        self.api_key = keys['api_key']
        self.private_key = keys['private_key']
        self.conn = None
        self.interface = None
        self.__connect()
        self.ignore_list = kwargs.get('ignore_list', [])
        self.exchange_name = kwargs.get('exchange_name', "kraken")
        self.asset_info = None
        self.last_asset_list = []
    
    def __del__(self):
        self.__disconnect()
    
    def __connect(self):
        self.__disconnect()
        self.log.info("Connecting to Kraken...")
        self.conn = krakenex.Connection()
        self.interface = krakenex.API(self.api_key, self.private_key, self.conn)
       
    def __disconnect(self):
        if self.interface is not None and self.conn is not None:
            self.log.debug("Closing connection to kraken")
            self.conn.close()
    
    """
    Returns the current time on the Exchange Server
    """
    def getExchangeServerTime(self):
        try:
            data = self.interface.query_public("Time")
            if (len(data['error']) == 0):
                return float(data['result']['unixtime']) / 1000.0
            else:
                self.log.error("An error was encountered retrieving the server time: "+str(data['error']))
        except Exception as e:
            self.log.error("Failed to retrieve server time.  Reason: "+str(e))
            self.log.debug(traceback.format_exc())
            self.__connect()
        return time.time()
    
    """
    Returns the current account balance of the user
    """
    def getAccountBalance(self):
        assetList = []
        try:
            data = self.interface.query_private("Balance")
            if (len(data['error']) == 0):
                if data['result'] is not None:
                    for asset in data['result']:
                        if asset not in self.ignore_list:
                            try:
                                assetList.append(AssetInfo(asset, float(data['result'][asset])))
                            except Exception as e:
                                self.log.error("Failed to retrieve account balance for "+str(asset))
                                self.log.debug(traceback.format_exc())
            else:
                self.log.error("An error was encountered accessing account: "+str(data['error']))
        except Exception as e:
            self.log.error("Failed to retrieve account balance. Reason: "+str(e))
            self.log.debug(traceback.format_exc())
            self.__connect()
        return assetList
    
    """
    Returns exchange data about the given asset pairs
    """
    def getAssetInfo(self, asset_list):
        if self.asset_info is None or self.last_asset_list is not asset_list:
            data = None
            assetList = []
            all_good = True
            #get data
            while data is None:
                try:
                    assetPairs=""
                    for asset in assetList:
                        assetPairs+=asset+","
                    assetPairs = assetPairs[:-1]
                    data = self.interface.query_public("AssetPairs", {"pair":assetPairs})
                except Exception as e:
                    self.log.error("Failed to retrieve asset info. Reason: "+str(e))
                    self.log.debug(traceback.format_exc())
                    self.__connect()
                    all_good = False
            #Format data
            if data is not None and (len(data['error']) == 0):
                if data['result'] is not None:
                    for ticker in data['result']:
                        try:
                            assetList.append(TickerInfo(self.exchange_name, ticker['base'], ticker['quote'], order_precision=ticker['pair_decimals']))
                        except Exception as e:
                            self.log.error("Failed to process asset info for "+str(asset))
                            self.log.debug(traceback.format_exc())
                            all_good = False
            else:
                self.log.error("An error was encountered retrieving asset info: "+str(data['error']))
            if all_good:
                self.asset_info = assetList
            return assetList
        else:
            return self.asset_info
    
    """
    Returns price data about the given asset pairs
    """
    def pollAssetPrices(self, asset_list):
        data = None
        assetList = []
        #get ticker data
        ticker_info = self.getAssetInfo(asset_list)
        pairs = {}
        for ticker in ticker_info:
            pairs[ticker.base+ticker.quote] = [ticker.base, ticker.quote]
        #get price data
        while data is None:
            try:
                assetPairs=""
                for asset in assetList:
                    assetPairs+=asset+","
                assetPairs = assetPairs[:-1]
                data = self.interface.query_public("AssetPairs", {"pair":assetPairs})
                if (len(data['error']) == 0):
                    return data['result']
                else:
                    self.log.error("An error was encountered retrieving asset info: "+str(data['error']))
                    return []   
            except Exception as e:
                self.log.error("Failed to retrieve asset info. Reason: "+str(e))
                self.log.debug(traceback.format_exc())
                self.__connect()
        #Format data
        if (len(data['error']) == 0):
            if data['result'] is not None:
                for ticker in data['result']:
                    try:
                        base, quote = pairs[asset['pair_name']]
                        assetList.append(TickerData(self.exchange_name, base, quote, 
                                                    ticker['a'][0], ticker['a'][1],
                                                    ticker['b'][0], ticker['b'][1]))
                    except Exception as e:
                        self.log.error("Failed to process asset info for "+str(asset))
                        self.log.debug(traceback.format_exc())
        else:
            self.log.error("An error was encountered retrieving asset info: "+str(data['error']))
        return assetList
    
    """
    Submit a list of orders to the exchange
    """
    def submitOrders(self, orders):
        resultList = []
        for order in orderList:
            try:
                if self.testmode:                    
                    order.success = True
                    resultList.append((order, {"txid":"testing"}))
                elif isinstance(order, Order) and (order.exchange == self.exchange_name):
                    data = self.interface.query_private("AddOrder",self.__formatOrder(order))
                    if (len(data['error']) == 0):
                        order.success = True
                        resultList.append((order, data['result']))
                    elif data['error'] == "The read operation timed out":   
                        #These may still be accepted by Kraken, but until
                        # we have a good way of handling them, just ignore them
                        # and re-sync the account records later
                        order.success = False
                        resultList.append((order, data['error']))
                    else:
                        order.success = False
                        resultList.append((order, data['error']))
                else:
                    order.success = False
                    resultList.append((order, {'error':"no data"}))
            except Exception as e:
                self.log.error("Failed to submit order of type "+str(type(order))+". Reason: "+str(e))
                self.log.debug(traceback.format_exc())
                self.__connect()
                order.success = False
                resultList.append((order, {'error':str(e)}))
        return resultList
        
    def __formatOrder(self, order):        
        if order.base is not None and order.quote is not None and order.action is not None \
            and order.price is not None and (order.volume > 0):
            order = {"pair":order.base+order.quote,
                     "type":order.action,
                     "ordertype":order.ordertype,
                     "price":order.price,
                     "volume":float(("{0:0."+str(order.precision)+"f}").format(order.volume)),
                     "oflags":order.feeFlag,
                     "expiretm":order.expiretime,
                     "userref":order.orderId}
            return order
        else:
            return dict()
    
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
    
    """
    Submits requests to transfer crypto currencies to different exchanges
    """
    def transferCurrency(self, transfer_requests):
        pass
    