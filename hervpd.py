# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn import svm
from sklearn.preprocessing import scale, StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit, GridSearchCV, train_test_split
from sklearn.metrics import classification_report


def filterActivities(df, includelist):
    return df.loc[df['activity'].isin(includelist)]

def excludeActivities(df, excludelist):
    return df.loc[~df['activity'].isin(excludelist)]

def userRows(df, user):
    userRows = df.loc[:,'user'] == user
    return df.loc[userRows,:]

def countExamplesByActivity(df):
    return df.groupby('activity').count()['user']

def addPartition(df, includelist, pname='partition', labelIn='in', labelOut='out'):
    l = []
    for x in df['activity'].isin(includelist):
        if x:
            l.append(labelIn)
        else:
            l.append(labelOut)
    args = {pname : l}
    return(df.assign(**args))


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
    dfs = [scaled_features(userRows(df, user).values, feature_cols) for user in df.user.unique()]
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
        dfu = userRows(df, user)
        dfus = scale_within_user(dfu, feature_cols)
        reports.append(run_flow(dfus, labelName), feature_cols)
        
    return reports    
    
