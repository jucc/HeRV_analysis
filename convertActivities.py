#!/bin/python
# -*- coding: utf-8 -*-

"""
Converts activities from old format to new format of sessions
Example -
OLD ACTIVITY (two events):
datetime,start,activity-category,posture
datetime,stop,,
NEW SESSION:
datetime-start,datetime-end,activity-name,posture,reliability,food-recent,caffeine-recent
"""

import os
import re
import csv
from datetime import datetime, timedelta


def getActivityFilenames():
    regexp = r"^act*"
    return list(filter(lambda x: re.match(regexp, x), os.listdir()))


def extractActivitiesFromFile(filename):
    lines = list(filter(lambda x : len(x) > 1, open(filename, 'r').readlines()))
    reader = csv.reader(lines, delimiter=',')
    rows = []
    sess = {}
    for row in reader:
        
        if isStartRow(row):
            # if there's an unfinished session pending, flush it first
            if sess.get('start') != None: 
                rows.append(sess)
            sess = startSession(row)
            
        elif isStopRow(row):
            # if there is no started session, ignore this stop command
            if sess.get('start') != None: 
                act = stopSession(row, sess)
                rows.append(act)
                sess = {}
            
        else:
            print ("Unidentified activity type in: %s"%row)
            
    return rows


def parseActivities(dirname):
    os.chdir(dirname)
    sessions = []
    for file in getActivityFilenames:
        sessions.extend(extractActivitiesFromFile(file))


def isStartRow(row):
    return (len(row) > 3 and row[1] == 'start')

def isStopRow(row):
    return (len(row) > 1 and row[1] == 'stop')

def timeFromString(timestr):
    return datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")

def startSession(row):
    sess = {'start': timeFromString(row[0]),
            'activity': row[2], 
            'posture': row[3] }
    if len(row) > 4:
        sess['notes'] = row[4]
    return sess
    
def stopSession(row, sess):
    sess['stop'] = timeFromString(row[0])
    return sess


if __name__ == '__main__':
    RAW_DATA_PATH = "C:\\Users\\julia\\Google Drive\\Academics\\Mestrado\\HeRV\\RawData\\0"
    os.chdir(RAW_DATA_PATH)
    #print(parseActivities(RAW_DATA_PATH))
    filename = 'act171013.csv'
    print (extractActivitiesFromFile(filename))
