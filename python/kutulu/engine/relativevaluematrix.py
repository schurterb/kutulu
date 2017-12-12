"""
@auther schurterb
@date 17-12-12
@description
 The core value matrix used by the engine.  Extrapolated to multiple exchanges and encapsulated for simplicity.
"""

import sys
sys.path.append("..")

import events
import logger

import numpy as np
import traceback


class RelativeValueMatrix:
    
    def __init__(self, exchanges, assets, **kwargs):
        self.log = logger.Logger("kutulu", "RelativeValueMatrix", "DEBUG")
        self.exchanges = exchanges
        self.exchange_list = {}
        for x in range(len(self.exchanges)):
            self.exchange_list[self.exchanges[x]] = x
        self.assets = assets
        self.asset_list = {}
        for x in range(len(self.assets)):
            self.asset_list[self.assets[x]] = x
        #Initialize the price matrix to -1 for all assets on all exchanges
        self.ask_price_matrix = np.ones((len(self.exchange_list), len(self.asset_list), len(self.asset_list))) * -1
        self.bid_price_matrix = np.ones((len(self.exchange_list), len(self.asset_list), len(self.asset_list))) * -1
        
   
    def updateRelativeValues(self, tickers):
        for ticker in tickers:
            #Backup old data
            old_ask = self.ask_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.base] ][ self.asset_list[ticker.quote] ]
            old_bid = self.bid_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.base] ][ self.asset_list[ticker.quote] ]
            old_ask_inverse = self.ask_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.quote] ][ self.asset_list[ticker.base] ]
            old_bid_inverse = self.bid_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.quote] ][ self.asset_list[ticker.base] ]
            try:
                #set new data
                self.ask_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.base] ][ self.asset_list[ticker.quote] ] = ticker.ask
                self.bid_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.base] ][ self.asset_list[ticker.quote] ] = ticker.bid
                self.ask_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.quote] ][ self.asset_list[ticker.base] ] = 1.0/ticker.ask
                self.bid_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.quote] ][ self.asset_list[ticker.base] ] = 1.0/ticker.bid
            except Exception as e:
                #if error, restore old data
                self.ask_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.base] ][ self.asset_list[ticker.quote] ] = old_ask
                self.bid_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.base] ][ self.asset_list[ticker.quote] ] = old_bid
                self.ask_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.quote] ][ self.asset_list[ticker.base] ] = old_ask_inverse
                self.bid_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.quote] ][ self.asset_list[ticker.base] ] = old_bid_inverse
                self.log.error("Failed to update matrix entries for exchange="+str(ticker.exchange)+" base="+str(ticker.base)+" quote="+str(ticker.quote)+".  Reason: "+str(e))
                self.log.debug(traceback.format_exc())
    
    def getAskPrice(self, exchange, base, quote):
        try:
            value = self.ask_price_matrix[ self.exchange_list[exchange] ][ self.asset_list[base] ][ self.asset_list[quote] ]
            if(value > 0.0):
                return value
        except Exception as e:
            self.log.error("Unable to retrieve an ask value for "+base+" - "+quote+" @ "+exchange+".  Reason: "+str(e))
            self.log.debug(traceback.format_exc())
        return None
        
    def getBidPrice(self, exchange, base, quote):
        try:
            value = self.bid_price_matrix[ self.exchange_list[exchange] ][ self.asset_list[base] ][ self.asset_list[quote] ]
            if(value > 0.0):
                return value
        except Exception as e:
            self.log.error("Unable to retrieve a bid value for "+base+" - "+quote+" @ "+exchange+".  Reason: "+str(e))
            self.log.debug(traceback.format_exc())
        return None
        
    