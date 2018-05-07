import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import parseIntervalFiles as pif

def clean_rr_series(rr, min=300, max=1800):
    """
    basic filter to remove clearly invalid interval values 
    intervals must be in the range 300 <= rr <= 1800
    """
    return [{'date': x['date'], 'interval': x['interval']} for x in rr if x['interval'] < max and x['interval'] > min]
    

def beats_to_lists(beatlist):
    """
    converts a list of beats (each item being a dict with two entries, date and interval)
    into two lists, one with the dates values and one with the intervals values
    Useful for plotting
    note: maybe python has a smart way to do this already?
    """
    xs = [(f['date'], f['interval']) for f in beatlist]
    return zip(*xs)


def get_clean_intervals(start, stop, user, path):
    """
    returns a list of intervals between start and stop for user without artifacts and outliers
    """
    dirname = path + "\\" + str(user)
    rr = pif.get_intervals(start, stop, dirname)    
    return clean_rr_series(rr)


def get_clean_intervals_from_dic(dic, path):
    """
    dic must be a dic or pandas row containing keys 'start', 'stop' and 'user'
    """
    return get_clean_intervals(dic['start'], dic['stop'], dic['user'], path)