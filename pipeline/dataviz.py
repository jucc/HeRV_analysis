import pandas as pd
import plotly.offline as pl
import plotly.graph_objs as go

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


def boxplot_compare(df, feature, groupby, min_examples=3):
    
    data = []

    for val in df[groupby].unique():
        if len(df[df[groupby]==val]) >= min_examples:
            data.append(go.Box(y=df.loc[df[groupby]==val, feature], name=val, showlegend=False))
        
    layout = go.Layout(yaxis=dict(title=feature, zeroline=False))
    fig = go.Figure(data=data, layout=layout)
    pl.iplot(fig)   