# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit, GridSearchCV, train_test_split
from sklearn.metrics import classification_report


def filter_in(df, column, include):
    return df.loc[df[column].isin(include)]

def filter_out(df, column, exclude):
    return df.loc[~df[column].isin(exclude)]

def count_by(df, column):
    return df.groupby(column).count()['user']

def user_data(df, user):
    return filter_in(df, 'user', [user])

def add_partition(df, includelist, pname='partition', labelIn='in', labelOut='out'):
    df[pname] = np.where(df['activity'].isin(includelist), labelIn, labelOut)
    return df

def scaled_features(df, feature_cols):
    """
    scales all features to a gausssian with mean = 0 and sd = 1
    """
    scaler = StandardScaler()
    return scaler.fit_transform(df[feature_cols].as_matrix())

def scale_within_user(df, feature_cols):
    """
    performs scaling (gaussian features eith mean = 0 and sd  = 1) separately 
    for each user, so that they don't affect each other's measures
    """
    dfs = [scaled_features(filter_in(df, 'user', [u]).values, feature_cols) for u in df.user.unique()]
    return pd.concat(dfs)


def report(testdf, result, labelName='activity', verbose=False):
    return classification_report([x for x in testdf[labelName]], result)
        

def run_flow(df, feature_cols, labelName='activity'):
    
    # preprocess dataset
    
    scaled_features(df, feature_cols)
    train, test = train_test_split(df, test_size=0.2)
    print("%d train examples and %d test examples"%(len(train),len(test)))        
    
    # define cross- validation and grid search parameters
    
    crossval = StratifiedShuffleSplit(n_splits=4, test_size=0.2)
    c_range = np.logspace(-2, 2, 5)
    gamma_range = np.logspace(-2, 2, 5)
    
    # linear kernel
    
    param_lin=dict(C=c_range)
    grid_lin = GridSearchCV(svm.SVC(kernel='linear', cache_size=1000), param_grid=param_lin, cv=crossval)
    grid_lin.fit(X=train[feature_cols], y=train[labelName])
    print("Best params for linear kernel: %s with score %0.5f" % (grid_lin.best_params_, grid_lin.best_score_))    
    clf1 = svm.SVC(kernel='linear', cache_size=1000, C=grid_lin.best_params_['C'])
    clf1.fit(X=train[feature_cols], y=train[labelName])
    print ('--- test results for linear kernel:')
    rl = report(test, clf1.predict(test[feature_cols]), labelName)
    print(rl)
        
    # rbf kernel
    
    param_rbf=dict(C=c_range, gamma=gamma_range)
    grid_rbf = GridSearchCV(svm.SVC(kernel='rbf', cache_size=1000), param_grid=param_rbf, cv=crossval)
    grid_rbf.fit(X=train[feature_cols], y=train[labelName])
    print("Best params for RBF kernel: %s with score %0.5f" % (grid_rbf.best_params_, grid_rbf.best_score_))
    clf2 = svm.SVC(kernel='rbf', cache_size=1000, C=grid_rbf.best_params_['C'], gamma=grid_rbf.best_params_['gamma'])    
    clf2.fit(X=train[feature_cols], y=train[labelName])
    print ('--- test results for RBF kernel:')
    rr = report(test, clf2.predict(test[feature_cols]), labelName)
    print(rr)   

    return [rl, rr]

    
def runFlowForEveryUser(df, feature_cols, labelName='activity'):
    reports = []
    for user in df.user.unique():
        dfu = user_data(df, user)
        dfus = scale_within_user(dfu, feature_cols)
        reports.append(run_flow(dfus, labelName), feature_cols)
        
    return reports    
    

def plot_count(df, label, include=[], exclude=[]):
    """
    generates a bar plot with the ciounts of df elements in column 'label'. 
    Optionally, only include rows where column values are in include list 
    or are outside exclude list
    """
    if len(include) != 0:
         df2 = df.loc[df.activity.isin(include)]
    elif len(exclude) != 0:
         df2 = df.loc[~df.activity.isin(exclude)]
    else:
         df2 = df
    ac = count_by(df2, label)
    ax = ac.plot(kind='bar')
    ax.set_ylabel("fragments")