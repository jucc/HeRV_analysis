import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def clean_rr_series(rr):
    """
    basic filter to remove clearly invalid interval values 
    intervals must be in the range 300 <= rr <= 1800
    """
    return [{'date': x['date'], 'interval': x['interval']} for x in rr if x['interval'] < 1800 and x['interval'] > 300]
