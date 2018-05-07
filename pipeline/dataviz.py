import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.offline as pl
pl.init_notebook_mode(connected=True)
import plotly.graph_objs as go

from datetime import datetime, timedelta
import parseIntervalFiles as pif
import parseActivityFiles as paf
#pun intended :)
import datacleaning as cl



def plot_series_with_hist(rr, title='timeseries'):
    """
    plots the series of RR intervals for user between start and stop datetimes
    """
    x1, x2 = cl.beats_to_lists(rr)

    trace1 = [go.Scatter(x=x1, y=x2)]
    trace2 = [go.Histogram(x=x2)]
    
    layout = go.Layout(title=title)

    pl.iplot(trace1, layout)
    pl.iplot(trace2, layout)


def plot_sess_rr(sess, path, title='Time series and Histogram'):
    """    
    sess can be a row from df or dic containing an 'rr' key with a list of beats (in dic form)
    """
    rr = cl.get_clean_intervals_from_dic(sess, path)
    plot_series_with_hist(rr)