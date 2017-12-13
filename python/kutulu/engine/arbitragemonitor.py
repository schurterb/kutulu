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
    
    def __init__(self, **kwargs):
        self.log = logger.Logger("kutulu", "ArbitrageMonitor", "DEBUG")
        
    def checkArbitrageOpportunities(self, relative_values):
        try:
            opportunities = []
            
            
        except Exception as e:
            self.log.error("Failed to check for arbitrage opportunities.  Reason: "+str(e))
            self.log.debug(traceback.format_exc())
                