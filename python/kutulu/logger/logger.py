# -*- coding: utf-8 -*-
"""
Created on Thu May  4 21:09:05 2017

@author: user

Logging module for platfrom
"""

from sh import mkdir
import logging
from logging.handlers import RotatingFileHandler

class Logger(object):
    
    def __init__(self, group, name, level=None, **kwargs):
        FORMAT = '%(asctime)s %(clientip)s %(levelname)s %(name)s : %(message)s'
        filepath = kwargs.get('logfile', 'log')
        if not filepath.endswith('/'):
            filepath = filepath + '/'
        mkdir('-p',filepath)
        self.clientip = kwargs.get('clientip','127.0.0.1')
        if name is not None:
            logfile = group+'.log'
            self.log = logging.getLogger(name)
        else:
            logfile = 'kutulu.log'
            self.log = logging.getLogger()
        self.formatter = logging.Formatter(FORMAT)
        handler = RotatingFileHandler(filepath+logfile,
                                      maxBytes=kwargs.get('max_file_bytes', 5242880),
                                      backupCount=kwargs.get('max_backups',100)) 
        handler.setFormatter(self.formatter)
        self.log.handlers.clear()
        self.log.addHandler(handler)
        self.log.setLevel(self.__getLevel(level))
        self.extras = {'clientip': self.clientip}
        
    def setDefaultLogLevel(self, level):
        level = self.__getLevel(level)
        logging.RootLogger.setLevel(logging.RootLogger, level=level)
        
    def critical(self, message, _exception=None, _traceback=None):
        if message is None:
            return
        if _exception is None:
            self.log.critical(message, extra=self.extras)
        else:
            self.log.critical(message +" :: "+self.formatter.formatException(_exception), extra=self.extras)
        if _traceback is not None:
            self.log.debug(_traceback, extra=self.extras)
            
    def error(self, message, _exception=None, _traceback=None):
        if message is None:
            return
        if _exception is None:
            self.log.error(message, extra=self.extras)
        else:
            self.log.error(message +" :: "+self.formatter.formatException(_exception), extra=self.extras)
        if _traceback is not None:
            self.log.debug(_traceback, extra=self.extras)
                        
    def warn(self, message):
        if message is not None:
            self.log.warning(message, extra=self.extras)
            
    def info(self, message):
        if message is not None:
            self.log.info(message, extra=self.extras)
            
    def debug(self, message):
        if message is not None:
            self.log.debug(message, extra=self.extras)
                        
    def __getLevel(self, level):
        levels = {
        'CRITICAL': logging.CRITICAL,
        'critical': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'error': logging.ERROR,
        'WARNING': logging.WARNING,
        'WARN': logging.WARNING,
        'warning': logging.WARNING,
        'warn': logging.WARNING,
        'INFO': logging.INFO,
        'info': logging.INFO,
        'DEBUG': logging.DEBUG,
        'debug': logging.DEBUG,
        'NOTSET': logging.NOTSET,
        'notset': logging.NOTSET,
        'NONE': logging.NOTSET,
        'none': logging.NOTSET,
        None: logging.NOTSET,
        }
        if level in levels.keys():
            return levels.get(level)
        else:
            return logging.NOTSET
