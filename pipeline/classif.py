import pandas as pd
import numpy as np

from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit, GridSearchCV, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix

import hervpd as hp


def report_binary(y_true, y_pred):    
    prf = precision_recall_fscore_support(y_true, y_pred, average='binary')
    cm = confusion_matrix(y_true, y_pred)
    return {'tn': cm[0][0], 'fn': cm[1][0], 'tp': cm[1][1], 'fp': cm[0][1],
            'precision': prf[0],  'recall': prf[1], 'f1': prf[2], 'support': prf[3]}


def fit_binary(clf, train, test, features, label):
    """
    http://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_fscore_support.html
    http://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
    """
    clf.fit(X=train[features], y=train[label])
    y_true = test[label]
    y_pred = clf.predict(X=test[features])
    result = report_binary(y_true, y_pred)
    score = clf.score(X=test[features], y=y_true)
    result.update({'label': label, 'score': score})
    return result


def fit_multiclass(clf, train, test, features, label):
    clf.fit(X=train[features], y=train[label])
    y_true = test[label]
    y_pred = clf.predict(X=test[features])
    result = report_binary(y_true, y_pred)
    score = clf.score(X=test[features], y=y_true)
    result.update({'label': label, 'score': score})
    return result


def multiclassifier_binary(classifiers, train, test, features, onehotlabels):
    results = []
    for key, clf in classifiers.items():
        for label in onehotlabels:
            f = fit_binary(clf, train, test, features, label)
            f.update({'classifier': key})
            results.append(f)
    return results


def full_binary_classification(classifiers, durations, crops, features, onehotlabels, user=-1, path='.'):
    results = []

    for dur in durations:
        for crop in crops:
            filename = build_filename(path, dur, crop)   
            print(filename)
            df = pd.read_excel(filename)
            print(len(df), 'frags')

            if user != -1:
                df = df.loc[df['user'] == user]
    
            train, test = hp.preprocess(df, onehotlabels)
    
            r = multiclassifier_binary(classifiers, train, test, features, onehotlabels)
            for f in r:
                f.update({'duration': dur, 'crop': crop, 'user': user})

            results.extend(r)

    return results    


def build_filename(path, dur, crop):
   return  path + '\\df_' + str(dur) + '_' + str(crop) + '_encoded.xlsx'


def build_filenames(path, durations, crops):
   return [build_filename(path, dur, crop) for dur in durations for crop in crops]