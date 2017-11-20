# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn import svm
from sklearn.preprocessing import scale
from sklearn.model_selection import StratifiedShuffleSplit, GridSearchCV, train_test_split
from sklearn.metrics import classification_report


def filterActivities(df, includelist):
    return df.loc[df['activity'].isin(includelist)]

def excludeActivities(df, excludelist):
    return df.loc[~df['activity'].isin(excludelist)]

def features(df):
    return df.iloc[:, 3:15]

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
    

# (side effect) scales all features od df to have mean = 0 and stdv = 1
def scaleFeatures(df):
    scaledFeatures = df.iloc[:, 3:15].apply(lambda x: scale(x)).values
    df.iloc[:, 3:15] = scaledFeatures
    

def scaleWithinUser(df):
    dfs = []
    for user in df.user.unique():
        u = userRows(df, user)
        u.iloc[:, 3:15] = u.iloc[:, 3:15].apply(lambda x: scale(x)).values
        dfs.append(u)
    return pd.concat(dfs)
    
    
def report(testdf, result, labelName='activity', verbose=False):
    ytrue = [x for x in testdf[labelName]]
    return classification_report(ytrue, result)
        

def runSVM(train, test, labelName, kernelName, grid_params, crossval):
    grid = GridSearchCV(svm.SVC(kernel=kernelName, cache_size=1000), param_grid=grid_params, cv=crossval)
    grid.fit(X=train.iloc[:, 3:15], y=train[labelName])
    print("Best params for %s kernel: %s with score %0.5f"%(kernelName, grid.best_params_, grid.best_score_))
    clf = svm.SVC(kernel=kernelName, cache_size=1000, C=grid.best_params_['C'])
    clf.fit(X=train.iloc[:, 3:15], y=train[labelName])
    print ('--- test results for linear kernel:')
    report(test, clf.predict(test.iloc[:, 3:15]), labelName)

def runFlow(df, labelName='activity'):
    
    # preprocess dataset
    
    scaleFeatures(df)
    train, test = train_test_split(df, test_size=0.2)
    print("%d train examples and %d test examples"%(len(train),len(test)))        
    
    # define cross- validation and grid search parameters
    
    crossval = StratifiedShuffleSplit(n_splits=4, test_size=0.2)
    c_range = np.logspace(-2, 2, 5)
    gamma_range = np.logspace(-2, 2, 5)
    
    # linear kernel
    
    param_lin=dict(C=c_range)
    grid_lin = GridSearchCV(svm.SVC(kernel='linear', cache_size=1000), param_grid=param_lin, cv=crossval)
    grid_lin.fit(X=train.iloc[:, 3:15], y=train[labelName])
    print("Best params for linear kernel: %s with score %0.5f" % (grid_lin.best_params_, grid_lin.best_score_))    
    clf1 = svm.SVC(kernel='linear', cache_size=1000, C=grid_lin.best_params_['C'])
    clf1.fit(X=train.iloc[:, 3:15], y=train[labelName])
    print ('--- test results for linear kernel:')
    rl = report(test, clf1.predict(test.iloc[:, 3:15]), labelName)
    print(rl)
        
    # rbf kernel
    
    param_rbf=dict(C=c_range, gamma=gamma_range)
    grid_rbf = GridSearchCV(svm.SVC(kernel='rbf', cache_size=1000), param_grid=param_rbf, cv=crossval)
    grid_rbf.fit(X=train.iloc[:, 3:15], y=train[labelName])
    print("Best params for RBF kernel: %s with score %0.5f" % (grid_rbf.best_params_, grid_rbf.best_score_))
    clf2 = svm.SVC(kernel='rbf', cache_size=1000, C=grid_rbf.best_params_['C'], gamma=grid_rbf.best_params_['gamma'])    
    clf2.fit(X=train.iloc[:, 3:15], y=train[labelName])
    print ('--- test results for RBF kernel:')
    rr = report(test, clf2.predict(test.iloc[:, 3:15]), labelName)
    print(rr)   

    return [rl, rr]

    
def runFlowForEveryUser(df, labelName='activity'):
    reports = []
    for user in df.user.unique():
        dfu = userRows(df, user)
        dfus = scaleWithinUser(dfu)
        reports.append(runFlow(dfus, labelName))
        
    return reports    
    
