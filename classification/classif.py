import pandas as pd
import numpy as np

from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit, GridSearchCV, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, precision_recall_fscore_support


def fit_and_report(clf, train, test, features, label):
    clf.fit(X=train[features], y=train[label])
    y_true = test[label]
    y_pred = clf.predict(X=test[features])
    score = clf.score(X=test[features], y=y_true)
    prf = precision_recall_fscore_support(y_true, y_pred)
    return {'label': label, 'score': score,  'prec_pos': prf[0][0], 'prec_neg': prf[0][1],  'rec_pos': prf[1][0], 'rec_neg': prf[1][1], 'f1_pos': prf[2][0], 'f1_neg': prf[2][1], 'sup_pos':prf[3][0], 'sup_neg': prf[3][1]}
    

def multiclassifiers(classifiers, train, test, features, onehotlabels):
    results = []
    for key, clf in classifiers.items():
        for label in onehotlabels:
            f = fit_and_report(clf, train, test, features, label)
            f.update({'classifier': key})
            results.append(f)
    return results

def build_filenames(path, croplist, durationlist):
   return  [ path + '\\df_' + str(dur) + '_' + str(crop) + '.xlsx' for dur in durationlist for crop in croplist ]