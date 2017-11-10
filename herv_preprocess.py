"""
Functions for running SVM classifier on the data (see jupyter notebook)
"""

import numpy as np
from sklearn import preprocessing


def getData(filename, dtype=None):
    return np.genfromtxt(filename, delimiter=',', dtype="i4,U20,U5,f4,f4,f4,f4,f4,f4,f4,f4,f4,f4,f4,f4", names=True)


def processData(data):    
    datagroups = getDataByActivity(data)    
    train, test = balanceTrainTestDatasets(datagroups)
    ltrain, ftrain = splitExamples(train)
    ltest, ftest = splitExamples(test)
    ftrain, ftest = scaleFeatures(ftrain, ftest)
    return (ltrain, ftrain, ltest, ftest)   
    

def getDataByActivity(data):
    return [[line for line in data if line['activity']==label] for label in np.unique(data['activity'])]


def balanceTrainTestDatasets(data, k=5):
    test  = []
    train = []
        
    for group in data:
        n = len(group)
        n_test = int(n/k)
        n_train = n - n_test    
        test.extend(group[0:n_test])
        train.extend(group[n_test:n])
        print ("%s: %d examples (%d for train and %d for test)"%(group[0]['activity'], n, n_train, n_test))

    print("\nTotal: %d train examples and %d test examples "%(len(train), len(test)))
    return(train, test)


def splitExamples(data, labelName='activity'):    
    examples = np.array([x.tolist()[3:] for x in data])
    labels = np.array([x[labelName] for x in data])
    return (labels, examples)


def scaleFeatures(ftrain, ftest):
    n_test = len(ftest)
    n_train = len(ftrain)
    f = np.vstack((ftrain, ftest))
    print("min and max values before scaling: ", np.min(f), np.max(f))
    f = preprocessing.scale(f)
    print("min and max values after scaling: ", np.min(f), np.max(f))
    return(f[0:n_train], f[n_train:n_train+n_test])


def filterActivities(data, includelist=None, excludelist=None):
    if includelist != None:
        return [line for line in data if line['activity'] in includelist]
    elif  excludelist != None:
        return [line for line in data if line['activity'] not in excludelist]
    else:
        return data
    # for filtering after grouping
    # groupsreturn [dg for dg in datagroups if dg[0]['activity'] in includelist]    


def groupActivities(data, group):
    for line in data:
        if line['activity'] in group:
            line['activity'] = 'in'
        else:
            line['activity'] = 'out'


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
    print("------\nGot %d out of %d right! :)"%(correct,len(expected)))