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
        self.ask_volume_matrix = np.ones((len(self.exchange_list), len(self.asset_list), len(self.asset_list))) * -1
        self.bid_price_matrix = np.ones((len(self.exchange_list), len(self.asset_list), len(self.asset_list))) * -1
        self.bid_volume_matrix = np.ones((len(self.exchange_list), len(self.asset_list), len(self.asset_list))) * -1
        
    def getExchangeNames(self):
        return self.exchanges
        
    def getAssetNames(self):
        return self.assets
   
    """
    Remember: (ask from BTC -> ETH) = 1/(bid from ETH -> BTC)
    """
    def updateRelativeValues(self, tickers):
        for ticker in tickers:
            if (ticker.ask > 0) and (ticker.bid > 0) and (ticker.ask_volume > 0) and (ticker.bid_volume > 0) and ticker.exchange in self.exchanges and ticker.base in self.assets and ticker.quote in self.assets:
                #Backup old data
                old_ask = self.ask_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.base] ][ self.asset_list[ticker.quote] ]
                old_bid = self.bid_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.base] ][ self.asset_list[ticker.quote] ]
                old_ask_inverse = self.ask_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.quote] ][ self.asset_list[ticker.base] ]
                old_bid_inverse = self.bid_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.quote] ][ self.asset_list[ticker.base] ]
                
                old_ask_volume = self.ask_volume_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.base] ][ self.asset_list[ticker.quote] ]
                old_bid_volume = self.bid_volume_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.base] ][ self.asset_list[ticker.quote] ]
                old_ask_volume_inverse = self.ask_volume_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.quote] ][ self.asset_list[ticker.base] ]
                old_bid_volume_inverse = self.bid_volume_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.quote] ][ self.asset_list[ticker.base] ]
                try:
                    #set new data
                    self.ask_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.base] ][ self.asset_list[ticker.quote] ] = ticker.ask
                    self.bid_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.base] ][ self.asset_list[ticker.quote] ] = ticker.bid
                    self.ask_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.quote] ][ self.asset_list[ticker.base] ] = 1.0/ticker.bid
                    self.bid_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.quote] ][ self.asset_list[ticker.base] ] = 1.0/ticker.ask
                    
                    self.ask_volume_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.base] ][ self.asset_list[ticker.quote] ] = ticker.ask_volume
                    self.bid_volume_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.base] ][ self.asset_list[ticker.quote] ] = ticker.bid_volume
                    self.ask_volume_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.quote] ][ self.asset_list[ticker.base] ] = ticker.ask_volume
                    self.bid_volume_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.quote] ][ self.asset_list[ticker.base] ] = ticker.bid_volume
                except Exception as e:
                    #if error, restore old data
                    self.ask_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.base] ][ self.asset_list[ticker.quote] ] = old_ask
                    self.bid_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.base] ][ self.asset_list[ticker.quote] ] = old_bid
                    self.ask_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.quote] ][ self.asset_list[ticker.base] ] = old_ask_inverse
                    self.bid_price_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.quote] ][ self.asset_list[ticker.base] ] = old_bid_inverse
                    
                    self.ask_volume_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.base] ][ self.asset_list[ticker.quote] ] = old_ask_volume
                    self.bid_volume_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.base] ][ self.asset_list[ticker.quote] ] = old_bid_volume
                    self.ask_volume_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.quote] ][ self.asset_list[ticker.base] ] = old_ask_volume_inverse
                    self.bid_volume_matrix[ self.exchange_list[ticker.exchange] ][ self.asset_list[ticker.quote] ][ self.asset_list[ticker.base] ] = old_bid_volume_inverse
                    self.log.error("Failed to update matrix entries for exchange="+str(ticker.exchange)+" base="+str(ticker.base)+" quote="+str(ticker.quote)+".  Reason: "+str(e))
                    self.log.debug(traceback.format_exc())
    
    def getAsk(self, exchange, base, quote):
        try:
            if exchange in self.exchanges and base in self.assets and quote in self.assets:
                value = self.ask_price_matrix[ self.exchange_list[exchange] ][ self.asset_list[base] ][ self.asset_list[quote] ]
                if(value > 0.0):
                    return value
            else:
                self.log.warn(exchange+" "+base+" "+quote+" are not a valid set of options for getting a ask value")
        except Exception as e:
            self.log.error("Unable to retrieve a ask value for "+str(base)+" - "+str(quote)+" @ "+str(exchange)+".  Reason: "+str(e))
            self.log.debug(traceback.format_exc())
        return None
        
    def getBid(self, exchange, base, quote):
        try:
            if exchange in self.exchanges and base in self.assets and quote in self.assets:
                value = self.bid_price_matrix[ self.exchange_list[exchange] ][ self.asset_list[base] ][ self.asset_list[quote] ]
                if(value > 0.0):
                    return value
            else:
                self.log.warn(exchange+" "+base+" "+quote+" are not a valid set of options for getting a bid value")
        except Exception as e:
            self.log.error("Unable to retrieve a bid value for "+str(base)+" - "+str(quote)+" @ "+str(exchange)+".  Reason: "+str(e))
            self.log.debug(traceback.format_exc())
        return None
     
    """
    return (ask + bid) / 2
    """
    def getAverage(self, exchange, base, quote):
        try:
            if exchange in self.exchanges and base in self.assets and quote in self.assets:
                ask = self.ask_price_matrix[ self.exchange_list[exchange] ][ self.asset_list[base] ][ self.asset_list[quote] ]
                bid = self.bid_price_matrix[ self.exchange_list[exchange] ][ self.asset_list[base] ][ self.asset_list[quote] ]
                if (ask > 0.0) and (bid > 0.0):
                    value = (ask + bid) / 2
                    if(value > 0.0):
                        return value
            else:
                self.log.warn(exchange+" "+base+" "+quote+" are not a valid set of options for getting an average value")
        except Exception as e:
            self.log.error("Unable to retrieve an average value for "+str(base)+" - "+str(quote)+" @ "+str(exchange)+".  Reason: "+str(e))
            self.log.debug(traceback.format_exc())
        return None
    
    """
    return ask - bid
    """   
    def getSpread(self, exchange, base, quote):
        try:
            if exchange in self.exchanges and base in self.assets and quote in self.assets:
                ask = self.ask_price_matrix[ self.exchange_list[exchange] ][ self.asset_list[base] ][ self.asset_list[quote] ]
                bid = self.bid_price_matrix[ self.exchange_list[exchange] ][ self.asset_list[base] ][ self.asset_list[quote] ]
                if (ask > 0.0) and (bid > 0.0):
                    value = ask - bid
                    if(value >= 0.0):
                        return value
            else:
                self.log.warn(exchange+" "+base+" "+quote+" are not a valid set of options for getting a value spread")
        except Exception as e:
            self.log.error("Unable to retrieve a spread value for "+str(base)+" - "+str(quote)+" @ "+str(exchange)+".  Reason: "+str(e))
            self.log.debug(traceback.format_exc())
        return None
    
    """
    return ( (ask * ask_volume) + (bid * bid_volume) ) / (ask_volume + bid_volume)
    """    
    def getWeightedAverage(self, exchange, base, quote):
        try:
            if exchange in self.exchanges and base in self.assets and quote in self.assets:
                ask = self.ask_price_matrix[ self.exchange_list[exchange] ][ self.asset_list[base] ][ self.asset_list[quote] ]
                bid = self.bid_price_matrix[ self.exchange_list[exchange] ][ self.asset_list[base] ][ self.asset_list[quote] ]
                ask_volume = self.ask_volume_matrix[ self.exchange_list[exchange] ][ self.asset_list[base] ][ self.asset_list[quote] ]
                bid_volume = self.bid_volume_matrix[ self.exchange_list[exchange] ][ self.asset_list[base] ][ self.asset_list[quote] ]
                if (ask > 0.0) and (bid > 0.0) and (ask_volume > 0.0) and (bid_volume > 0.0):
                    value = ( (ask * ask_volume) + (bid * bid_volume) ) / (ask_volume + bid_volume)
                    if(value > 0.0):
                        return value
            else:
                self.log.warn(exchange+" "+base+" "+quote+" are not a valid set of options for getting a weighted average value")
        except Exception as e:
            self.log.error("Unable to retrieve an average value for "+str(base)+" - "+str(quote)+" @ "+str(exchange)+".  Reason: "+str(e))
            self.log.debug(traceback.format_exc())
        return None
    
    """
    return ( (ask * ask_volume) - (bid * bid_volume) ) / (ask_volume - bid_volume)
    """
    def getWeightedSpread(self, exchange, base, quote):
        try:
            if exchange in self.exchanges and base in self.assets and quote in self.assets:
                ask = self.ask_price_matrix[ self.exchange_list[exchange] ][ self.asset_list[base] ][ self.asset_list[quote] ]
                bid = self.bid_price_matrix[ self.exchange_list[exchange] ][ self.asset_list[base] ][ self.asset_list[quote] ]
                ask_volume = self.ask_volume_matrix[ self.exchange_list[exchange] ][ self.asset_list[base] ][ self.asset_list[quote] ]
                bid_volume = self.bid_volume_matrix[ self.exchange_list[exchange] ][ self.asset_list[base] ][ self.asset_list[quote] ]
                if (ask > 0.0) and (bid > 0.0) and (ask_volume > 0.0) and (bid_volume > 0.0):
                    value = ( (ask * ask_volume) - (bid * bid_volume) ) / (ask_volume - bid_volume)
                    if(value >= 0.0):
                        return value
            else:
                self.log.warn(exchange+" "+base+" "+quote+" are not a valid set of options for getting a weighted value spread")
        except Exception as e:
            self.log.error("Unable to retrieve a spread value for "+str(base)+" - "+str(quote)+" @ "+str(exchange)+".  Reason: "+str(e))
            self.log.debug(traceback.format_exc())
        return None