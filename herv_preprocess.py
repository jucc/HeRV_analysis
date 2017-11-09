"""
Functions for running SVM classifier on the data (see jupyter notebook)
"""

import numpy as np
from sklearn import preprocessing


def getData(filename, dtype):    
    data = getFileContents(filename, dtype)    
    return preprocess(data, 'activity')


def getFileContents(filename, dtype):
    return np.genfromtxt(filename, delimiter=',', dtype=dtype, names=True)


def preprocess(data, labelName):    
    labels = np.array([x[labelName] for x in data])    
    examples = np.array([x.tolist()[3:23] for x in data])
    print("(#samples, #features) = ", examples.shape)
    print("min and max values before scaling: ", np.min(examples), np.max(examples))
    examples = preprocessing.scale(examples)
    print("min and max values after scaling: ", np.min(examples), np.max(examples))
    return (labels, examples)


def convertToDic(labels, examples):
    dic = [{'activity': label, 'examples': examples[labels==label]} for label in np.unique(labels)]
    return dic


def addHierarchyLabels(dic):
    for sess in dic:
        if sess['activity'] in ('movement', 'household-chores', 'exercise-high', 'exercise-low'):
            sess['l1-movement'] = 1
        else:
            sess['l1-movement'] = 0
    return dic


def generateSets(labels, examples, k):

    ltest  = []
    ltrain = []
    ftest  = []
    ftrain = []    
    
    dic = convertToDic(labels, examples)
    labelName = 'activity'

    for activity in dic:
        n = len(activity['examples'])
        n_test = int(n/k)
        n_train = n - n_test    
        ltest.extend([activity[labelName] for i in range(n_test)])
        ltrain.extend([activity[labelName] for i in range(n_train)])
        ftest.extend(activity['examples'][0:n_test])
        ftrain.extend(activity['examples'][n_test:n])
        print ("%s: %d examples (%d for train and %d for test)"%(activity[labelName], n, n_train, n_test))

    print("\nTotal: %d train examples and %d test examples "%(len(ftrain), len(ftest)))
    return(ltrain, ltest, ftrain, ftest)


def printResults(expected, result):
    print("expected\t\tresult")
    print("------------------------------")
    correct = 0
    for i in range(len(expected)):
        print ("%s\t\t%s"%(expected[i], result[i]))
        if expected[i] == result[i]:
            correct += 1    
    print("------\nGot %d out of %d right! :)"%(correct,len(expected)))