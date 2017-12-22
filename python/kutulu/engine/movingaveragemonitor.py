"""
@auther schurterb
@date 17-12-22
@description
 The basic class for monitoring the exponential moving averages of different
 lengths forvarious asset pairs. These calculations are started without a history, 
 so the first n values are unreliable where n is the period of the moving average.
 The equations for this EMA are calculated as follows:
    multiplier = 2 / (period + 1)
    ema = ((latest_price - ema) * multiplier) + ema
"""

import sys
sys.path.append("..")

import events
import logger

import numpy as np
import traceback
import time

class MovingAverageMonitor:
    
    def __init__(self, periods, exchanges, assets, **kwargs):
        self.log = logger.Logger("kutulu", "MovingAverageMonitor", "DEBUG")
        self.log.debug("Initializing MovingAverageMonitor")
        self.exchanges = exchanges
        self.exchange_list = {}
        for x in range(len(self.exchanges)):
            self.exchange_list[self.exchanges[x]] = x
        self.assets = assets
        self.asset_list = {}
        for x in range(len(self.assets)):
            self.asset_list[self.assets[x]] = x
        self.periods = np.asarray(periods) * 60 #Int
        self.moving_average_tables = {}
        self.moving_average_timers = {}
        for period in self.periods:
            self.moving_average_tables[period] = np.zeros((len(self.exchanges), len(self.assets), len(self.assets)))
            self.moving_average_timers[period] = time.time()
        self.log.debug("Finished initializing MovingAverageMonitor")
        
    def getPeriods(self):
        return self.periods
        
    def getMovingAverage(self, exchange, base, quote, period):
        if exchange in self.exchanges and base in self.assets and quote in self.assets and period in self.periods:
            return self.moving_average_tables[ period ][ self.exchange_list[exchange] ][ self.asset_list[base] ][ self.asset_list[quote] ]
            
    def updateMovingAverage(self, rvm):
        self.log.debug("Updating moving averages")
        try:
            for period in self.periods:
                if (time.time() - self.moving_average_timers[period]) > period:
                    self.moving_average_timers[period] = time.time()
                    multiplier = 2 / (period + 1)
                    for exchange in self.exchanges:
                        for base in self.assets:
                            for quote in self.assets:
                                try:
                                    price = rvm.getWeightedAverage(exchange, base, quote)
                                    if price is not None:
                                        ema = self.moving_average_tables[ period ][ self.exchange_list[exchange] ][ self.asset_list[base] ][ self.asset_list[quote] ]
                                        ema = ((price - ema) * multiplier) + ema
                                        self.moving_average_tables[ period ][ self.exchange_list[exchange] ][ self.asset_list[base] ][ self.asset_list[quote] ] = ema
                                    else:
                                        self.log.warn("No value was found for "+str(base)+str(quote)+" at "+str(exchange))
                                except Exception as e:
                                    self.log.error("Failed to update moving average for "+str(base)+str(quote)+" at "+str(exchange)+".  Reason: "+str(e))
                                    self.log.debug(traceback.format_exc())
        except Exception as e:
            self.log.error("Failed to update moving averages.  Reason: "+str(e))
            self.log.debug(traceback.format_exc())
        self.log.debug("Finished updating moving averages")
            