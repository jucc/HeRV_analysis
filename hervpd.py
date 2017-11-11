# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn import svm
from sklearn.preprocessing import scale
from sklearn.model_selection import StratifiedShuffleSplit, GridSearchCV, train_test_split



def filterActivities(df, includelist):
    return df.loc[df['activity'].isin(includelist)]

def excludeActivities(df, excludelist):
    return df.loc[~df['activity'].isin(excludelist)]

def features(df):
    return df.iloc[:, 3:15]


def printResults(expected, result, verbose=False):
    if verbose: 
        print("expected\t\tresult")
        print("------------------------------")
    correct = 0
    for i in range(len(expected)):
        if verbose:
            print ("%s\t\t%s"%(expected[i], result[i]))
        if expected[i] == result[i]:
            correct += 1    
    print("%d out of %d right! :)"%(correct,len(expected)))


def runFlow(df):    
    df.iloc[:, 3:15] = df.iloc[:, 3:15].apply(lambda x: scale(x))
    train, test = train_test_split(df, test_size=0.2)
    print("%d train examples and %d test examples"%(len(train),len(test)))
    crossval = StratifiedShuffleSplit(n_splits=4, test_size=0.2)
    c_range = np.logspace(-1, 2, 4) 
    gamma_range = np.logspace(-2, 1, 4)
    param_lin=dict(C=c_range)
    param_rbf=dict(C=c_range, gamma=gamma_range)
    grid_lin = GridSearchCV(svm.SVC(kernel='linear', cache_size=1000), param_grid=param_lin, cv=crossval)
    grid_lin.fit(X=train.iloc[:, 3:15], y=train['activity'])
    print("Best params for linear kernel: %s with score %0.5f" % (grid_lin.best_params_, grid_lin.best_score_))
    grid_rbf = GridSearchCV(svm.SVC(kernel='rbf', cache_size=1000), param_grid=param_rbf, cv=crossval)
    grid_rbf.fit(X=train.iloc[:, 3:15], y=train['activity'])
    print("Best params for RBF kernel: %s with score %0.5f" % (grid_rbf.best_params_, grid_rbf.best_score_))
    clf1 = svm.SVC(kernel='linear', cache_size=1000, C=grid_lin.best_params_['C'])
    clf1.fit(X=train.iloc[:, 3:15], y=train['activity'])
    print ('--- test results for linear kernel:')
    printResults(test['activity'].values, clf1.predict(test.iloc[:, 3:15]))
    clf2 = svm.SVC(kernel='rbf', cache_size=1000, C=grid_rbf.best_params_['C'], gamma=grid_rbf.best_params_['gamma'])    
    clf2.fit(X=train.iloc[:, 3:15], y=train['activity'])
    print ('--- test results for RBF kernel:')
    printResults(test['activity'].values, clf1.predict(test.iloc[:, 3:15]))

    
    
    

    
    