from time import strftime, gmtime
import datetime

def hourTimestamp():
    """get current hour (GMT+0) but its shorter and cleaner"""
    ret = strftime("%H:%M:%S", gmtime())
    return ret