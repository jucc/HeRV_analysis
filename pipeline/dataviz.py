import pandas as pd
import plotly.offline as pl
import plotly.graph_objs as go
from plotly import tools

import datacleaning as cl

"""
SERIES AND FEATURES DATAVIZ FOR SESSIONS/FRAGMENTS/CONTINUOUS TIME
"""

def plot_series(rr, hist=True):
    """
    plotly traces for the series of RR intervals for user between start and stop datetimes
    and, optionally, its distribution histogram
    """
    x1, x2 = cl.beats_to_lists(rr)
    return [go.Scatter(x=x1, y=x2)]


def plot_sess_series(sess, path, hist=True):
    """
    plotly trace for the cleaned up rr series contained in sess, where sess can be either
    a DataFrame row or any dic containing an 'rr' key with a list of beats
    """
    rr = cl.get_clean_intervals_from_dic(sess, path)
    return plot_series(rr, hist)


def plot_features(frags, activities, filter=1):
    """
    plotly trace for the evolution of features in contiguous fragments,
    optionally filtered through a moving median
    """
    if filter > 1:
        if filter%2 == 0:
            filter = filter+1
    else:
        filter = 1

    copy = frags.copy() # use a copy to smooth so that original data is not altered    
    for activity in activities:
        if filter > 1:
            copy[activity] = copy[activity].rolling(window=filter, center=True).median()

    return [go.Scatter(x=copy['f_id'], y=copy[activity], name=activity) for activity in activities]


def plot_sess_features(sess, fdf, feats=['rmssd', 'mhr', 'sdnn', 'pnn50']):
    """
    plotly trace for the evolution of features in a session
    """
    pp = fdf.loc[fdf['sess_id'] == sess['sess_id']].sort_values(by=['f_id'], ascending=True)
    return plot_features(pp, feats, filter=1)


def full_plot_sess(sess, fdf, path):
    """
    actually plots the time series and features for a given session
    TODO still needs the frag db as an argument, improve later
    """
    print ("SESSION ID: ", sess['sess_id'])
    print ("ACTIVITY: "  , sess['activity'])
    print ("USER: "  , sess['user'])
    print ("TIME: "  , sess['start'])

    tr1 = plot_sess_series(sess, path, hist=False)
    tr2 = plot_sess_features(sess, fdf)

    pl.iplot(tr1)
    pl.iplot(tr2)

    

"""
GROUPED VIEWS OF FEATURES
"""

def boxplot_compare(df, feature, groupby, min_examples=3):    
    data = []

    for val in df[groupby].unique():
        if len(df[df[groupby]==val]) >= min_examples:
            data.append(go.Box(y=df.loc[df[groupby]==val, feature], name=val, showlegend=False))
        
    layout = go.Layout(yaxis=dict(title=feature), xaxis=dict(title=groupby))
    fig = go.Figure(data=data, layout=layout)
    pl.iplot(fig)



"""
GRAPHS IN RESULTS PRESENTATIONS
"""

def bargroup(df, d1, d2, d3, dz):

    for x1 in df[d1].unique():
    
        ddf = df.loc[df[d1] == x1]
        
        data = []
        for x2 in df[d2].unique():        
            ndf = ddf.loc[ddf[d2] == x2]
            data.append(go.Bar(x=ndf[d3], y=ndf[dz], name=x2))

        layout = go.Layout(barmode='group', title=x1)
        fig = go.Figure(data=data, layout=layout)
        pl.iplot(fig)


def bar_results(df, d1, d2, d3, dz):

    for x1 in df[d1].unique():
    
        ddf = df.loc[df[d1] == x1]
        
        data = []
        for x2 in df[d2].unique():        
            ndf = ddf.loc[ddf[d2] == x2]
            data.append(go.Bar(x=ndf[d3], y=ndf[dz], name=x2))

        layout = go.Layout(barmode='group', title=x1)
        fig = go.Figure(data=data, layout=layout)
        pl.iplot(fig)


