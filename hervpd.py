# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 21:15:23 2017

@author: julia
"""


def filterActivities(df, includelist)
    return df[df['activity'].isin(includelist)]

def excludeActivities(df, excludelist)
    return df[~df['activity'].isin(includelist)]

def getFeaturesOnly(df):
    return df.iloc[:, 3:15]

