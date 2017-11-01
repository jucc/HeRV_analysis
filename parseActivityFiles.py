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

import csvUtils as csvu
from datetime import datetime


"""
extract list of sessions from all activity files in a dir
"""
def parseActivityFiles(dirname):
    sessions = []
    errors = 0  
    files = list(csvu.getFilenames(dirname, r"^act.*"))
    for file in files:
        print('reading %s ... '%file.split('\\')[-1])
        (f_sessions, f_errors) = extractSessions(file)
        sessions.extend(f_sessions)
        errors += f_errors    
    print ("%d sessions extracted and %d errors found in %d files"
           %(len(sessions), errors, len(files)))
    return sessions


"""
extract list of sessions from an activity file
"""
def extractSessions(filename):    
    sessions = []    
    sess = {}
    excluded = 0
    reader = csvu.getFileReader(filename)
    for row in reader:
        
        if isStartRow(row) and not started(sess):
            sess = startSession(row)
            
        elif isStopRow(row) and started(sess):
            sessions.append(stopSession(row, sess))
            sess = {}
            
        else:
            if isStartRow(row) and started(sess):
                msg = 'orphan start in: %s'
            elif isStopRow(row) and not started(sess):
                msg = 'orphan stop in: %s'            
            else:
                msg = 'unidentified activity type in: %s'                
            excluded += 1
            print (msg%row)
    
    return (sessions, excluded)


def isStartRow(row):
    return (len(row) > 3 and row[1] == 'start')

def isStopRow(row):
    return (len(row) > 1 and row[1] == 'stop')

def started(sess):
     return (sess.get('start') != None)
 
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
    sessions = parseActivityFiles(RAW_DATA_PATH)        
    print('first session:')
    print(sessions[0])
    
