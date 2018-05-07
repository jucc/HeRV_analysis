import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


def clean_rr_series(rr, min=300, max=1800):
    """
    basic filter to remove clearly invalid interval values 
    intervals must be in the range 300 <= rr <= 1800
    """
    return [{'date': x['date'], 'interval': x['interval']} for x in rr if x['interval'] < max and x['interval'] > min]
