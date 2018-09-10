import pandas as pd
import numpy as np

from sklearn import svm
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix, accuracy_score

import plotly.offline as pl
import plotly.graph_objs as go

import hervpd as hp
import classif


def fit_test(clf, df, features, label='activity'):

    train, test = hp.preprocess(df, features)

    clf.fit(X=train[features], y=train[label])
    y_true = test[label]
    y_pred = clf.predict(X=test[features])

    return (y_true, y_pred)


def unique_classes(ytrue):
    classes = ytrue.unique()
    classes.sort()
    return classes


def prfs_heatmap(ytrue, ypred, cs='RdBu'):
    classes = unique_classes(ytrue)
    metrics = ['precision', 'recall', 'f1']
    prf = np.array(precision_recall_fscore_support(ytrue, ypred)[:][0:3]).transpose()
    blueisgood=[[0.0, 'rgb(165,0,38)'], [0.1111111111111111, 'rgb(215,48,39)'], 
                [0.2222222222222222, 'rgb(244,109,67)'], [0.3333333333333333, 'rgb(253,174,97)'], 
                [0.4444444444444444, 'rgb(254,224,144)'], [0.5555555555555556, 'rgb(224,243,248)'], 
                [0.6666666666666666, 'rgb(171,217,233)'], [0.7777777777777778, 'rgb(116,173,209)'], 
                [0.8888888888888888, 'rgb(69,117,180)'], [1.0, 'rgb(49,54,149)']]
    data = [go.Heatmap(z=prf, y=classes, x=metrics, colorscale=blueisgood,
                       zmin=0.5, zmax=1.0)]

    layout = go.Layout(title = 'Precision, Recall, F1-score', 
                       font = dict (size=16, color='#333333'), 
                       yaxis = dict(autorange='reversed'))

    return go.Figure(data=data, layout=layout)


def cmatrix_heatmap(ytrue, ypred):
    classes = unique_classes(ytrue)

    whiteisnone=[[0.0, 'rgb(255,255,255)'], [0.1, 'rgb(190,245,235)'], 
                 [0.2, 'rgb(170,225,215)'], [0.3, 'rgb(150,205,195)'], 
                 [0.4, 'rgb(130,185,175)'], [0.5, 'rgb(110,165,155)'], 
                 [0.6, 'rgb(90,145,135)'], [0.7, 'rgb(70,125,115)'], 
                 [0.8, 'rgb(50,105,95)'], [0.9, 'rgb(30,85,75)'],
                 [1.0, 'rgb(10,65,55)']]
    
    
    data = [go.Heatmap(z=confusion_matrix(ytrue, ypred, classes),
                       x=classes, y=classes, colorscale=whiteisnone)]

    layout = go.Layout(
        title = 'Confusion Matrix',
        font = dict (size=16, color='#333333'),
        xaxis = dict(title='predicted',
                     titlefont=dict(size=16, color='#333333')),
        yaxis = dict(title='true label',
                     titlefont=dict(size=16, color='#333333'),
                     autorange='reversed'))

    return go.Figure(data=data, layout=layout)


def prf_user(clf, df, user, features, label='activity'):
    dfx = df.loc[df['user'] == user]
    ytrue, ypred = fit_test(clf, dfx, features, label)
    return prfs_heatmap(ytrue, ypred)


def prfs_report(ytrue, ypred):
    classes = unique_classes(ytrue)
    prf = precision_recall_fscore_support(ytrue, ypred)
    result = []
    for i, cl in enumerate(classes):         
        result.append({ 'class': cl, 'precision': prf[0][i],  'recall': prf[1][i], 
                        'f1': prf[2][i], 'support': prf[3][i]})
    return result


def classif_summary(clf, df, features, label):
    yt, yp = fit_test(clf, df, features, label)
    return prfs_report(yt, yp)


def multiclass_classif_table(durations, crops, classifiers, features, label, path, user=-1):
    res = []
    for duration in durations:
        for crop in crops:
            filename = build_filename(path, duration, crop)
            dfi = pd.read_excel(filename)
            dfi = dfi[dfi['gr_main3'].isin(['still', 'sleep', 'move'])]
            for key, clf in classifiers.items():
                if user != -1:
                    dfi = dfi.loc[dfi['user']==user]
                dcr = classif_summary(clf, dfi, features, label)
                for x in dcr:
                    x.update( {'classifier':key, 'duration':duration, 'crop': crop, 'label': label, 'user': user} )
                    res.append(x)                
    return res


def build_filename(path, dur, crop):
   return  path + '\\df_' + str(dur) + '_' + str(crop) + '_grouped.xlsx'


def plot_matrices(df, clf, features, label):

    print ("\n\n\n---------------------------------------------", label, "---------------------------------------------")
    print (hp.count_by(df=df, column=label))
    ytrue, ypred = fit_test(clf, df, features, label)
    pl.iplot(prfs_heatmap(ytrue, ypred))
    pl.iplot(cmatrix_heatmap(ytrue, ypred))


def barplot_accuracy_per_user(df, clf, features, label, users):
    data = []
    for user in users:
        ytrue, ypred = fit_test(clf, df[df.user==user], features, label)
        data.append(accuracy_score(ytrue, ypred))        
    
    fig = [go.Bar(y=data)]
    pl.iplot(fig)

