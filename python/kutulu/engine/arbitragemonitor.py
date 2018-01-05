"""
@auther schurterb
@date 17-12-12
@description
 The basic class for monitoring cross-exchange trends and calculating when to perform arbitrage
"""

import sys
sys.path.append("..")

import events
import logger

import numpy as np
import traceback


class ArbitrageMonitor:
    
    def __init__(self, config, **kwargs):
        self.log = logger.Logger("kutulu", "ArbitrageMonitor", "DEBUG")
        self.log.debug("Initializing ArbitrageMonitor")
        self.network_fee = config.get("network_fees")
        self.exchange_fee = config.get("exchange_fees")
        self.log.debug("Finished initializing ArbitrageMonitor")
        
    """
    Returns a list of arbitrage opportunities between exchanges.
    Each list entry is formatted thus:
        (<buy exchange> <sell exchange> <base asset> <quote asset>)
    """
    def checkArbitrageOpportunities(self, rvm):
        self.log.debug("Searching for arbitrage opportunities")
        opportunities = []
        try:
            for buy_exchange in rvm.getExchangeNames():
                for sell_exchange in rvm.getExchangeNames():
                    for base in rvm.getAssetNames():
                        for quote in rvm.getAssetNames():
                            try:
                                buy_price = rvm.getWeightedAverage(buy_exchange, base, quote)
                                sell_price = rvm.getWeightedAverage(sell_exchange, base, quote)
                                print(sell_price,self.exchange_fee[sell_exchange],buy_price,self.exchange_fee[buy_exchange])
                                if( (sell_price * self.exchange_fee[sell_exchange]) - (buy_price * self.exchange_fee[buy_exchange]) > (self.network_fee * 2) ):
                                    opportunities.append([buy_exchange, sell_exchange, base, quote])
                            except Exception as e:
                                self.log.error("Error while checking arbitrage between "+str(buy_exchange)+" and "+str(sell_exchange)+".  Reason: "+str(e))
                                self.log.debug(traceback.format_exc())
        except Exception as e:
            self.log.error("Failed to check for arbitrage opportunities.  Reason: "+str(e))
            self.log.debug(traceback.format_exc())
        self.log.debug("Found "+str(len(opportunities))+" arbitrage opportunities")
        return opportunities
                