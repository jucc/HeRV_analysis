import pandas as pd
import numpy as np

from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit, GridSearchCV, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, precision_recall_fscore_support

import hervpd as hp


def fit_and_report(clf, train, test, features, label):
    clf.fit(X=train[features], y=train[label])
    y_true = test[label]
    y_pred = clf.predict(X=test[features])
    score = clf.score(X=test[features], y=y_true)
    prf = precision_recall_fscore_support(y_true, y_pred)
    return {'label': label, 'score': score,  'prec_pos': prf[0][0], 'prec_neg': prf[0][1],  'rec_pos': prf[1][0], 'rec_neg': prf[1][1], 'f1_pos': prf[2][0], 'f1_neg': prf[2][1], 'sup_pos':prf[3][0], 'sup_neg': prf[3][1]}
    

def multiclassifier(classifiers, train, test, features, onehotlabels):
    results = []
    for key, clf in classifiers.items():
        for label in onehotlabels:
            f = fit_and_report(clf, train, test, features, label)
            f.update({'classifier': key})
            results.append(f)
    return results


def full_classification(classifiers, durations, crops, features, onehotlabels, user=-1, path='.'):
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
    
            r = multiclassifier(classifiers, train, test, features, onehotlabels)
            for f in r:
                f.update({'duration': dur, 'crop': crop})

            results.extend(r)

    return results    


def build_filename(path, dur, crop):
   return  path + '\\df_' + str(dur) + '_' + str(crop) + '_encoded.xlsx'


def build_filenames(path, durations, crops):
   return [build_filename(path, dur, crop) for dur in durations for crop in crops]