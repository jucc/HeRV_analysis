# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotReport as pr

from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit, GridSearchCV, train_test_split
from sklearn.ensemble import RandomForestClassifier
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


def scaled_features(df, feature_cols):
    """
    scales all features to a gausssian with mean = 0 and sd = 1
    """
    scaler = StandardScaler()
    return scaler.fit_transform(df[feature_cols].as_matrix())

def preprocess(df, features):
    """
    scales all features and splits df into train (4/5 examples)
    and test (1/5) datasets
    """
    scaled_features(df, features)
    train, test = train_test_split(df, test_size=0.2)
    print(len(train), len(test))
    return (train, test)

def report_test(clf, df_test, features, labels, print_report=False, plot_report=False):
    """
    returns the calulated score of classifier in the test dataset and,
    optionally, prints the f1 report and its heatmap plot
    """
    y_true = df_test[labels]
    y_pred = clf.predict(X=df_test[features])
    if len(labels) > 1:
        label_names = labels
    else:
        label_names = ['not ' + labels[0], labels[0]] 
    report = classification_report(y_true, y_pred, target_names=label_names)
    if print_report:
        print(report)
    if plot_report:
        pr.plot_classification_report(report, cmap=plt.cm.coolwarm_r)
    return clf.score(X=df_test[features], y=y_true)


def clf_svm_lin(df_train, feature_cols, labelName='activity', C=10):
    """
    create and fit a linear svm classifier
    """
    clf1 = svm.SVC(kernel='linear', cache_size=1000, C=C)
    clf1.fit(X=df_train[feature_cols], y=df_train[labelName])
    return clf1

def clf_svm_rbf(df_train, feature_cols, labelName='activity', C=10, gamma=0.1):
    """
    create and fit a rbf svm classifier
    """
    clf1 = svm.SVC(kernel='rbf', cache_size=1000, C=C, gamma=gamma)
    clf1.fit(X=df_train[feature_cols], y=df_train[labelName])
    return clf1

def clf_rf(df_train, features, labels):  
    """
    create and fit a random forest classifier
    """
    clf = RandomForestClassifier(n_estimators=100, n_jobs=-1)
    clf.fit(X=df_train[features], y=df_train[labels])
    return clf


def model_selection_svm(df, feature_cols, labelName='activity'):

    train, test = preprocess(df, feature_cols)

    # define cross- validation and grid search parameters

    crossval = StratifiedShuffleSplit(n_splits=4, test_size=0.2)
    c_range = np.logspace(-2, 2, 5)
    gamma_range = np.logspace(-2, 2, 5)

    # linear kernel

    param_lin=dict(C=c_range)
    grid_lin = GridSearchCV(svm.SVC(kernel='linear', cache_size=1000), param_grid=param_lin, cv=crossval)
    grid_lin.fit(X=train[feature_cols], y=train[labelName])
    print("Best params for linear kernel: %s with score %0.5f" % (grid_lin.best_params_, grid_lin.best_score_))    
        
    # rbf kernel
    
    param_rbf=dict(C=c_range, gamma=gamma_range)
    grid_rbf = GridSearchCV(svm.SVC(kernel='rbf', cache_size=1000), param_grid=param_rbf, cv=crossval)
    grid_rbf.fit(X=train[feature_cols], y=train[labelName])
    print("Best params for RBF kernel: %s with score %0.5f" % (grid_rbf.best_params_, grid_rbf.best_score_))

    return (grid_lin.best_params_['C'], grid_rbf.best_params_['C'], grid_rbf.best_params_['gamma'])