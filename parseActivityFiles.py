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


"""
extract list of sessions from all activity files in a dir
"""
def parseActivityFiles(dirname, verbose=True):
    sessions = []
    errors = 0  
    files = list(csvu.getFilenames(dirname, r"^act.*"))
    for file in files:
        if verbose:
            print('reading %s ... '%file.split('\\')[-1])
        (f_sessions, f_errors) = extractSessions(file, verbose)
        sessions.extend(f_sessions)
        errors += f_errors    
    
    if verbose:
        print ("%d sessions extracted and %d errors found in %d files"
               %(len(sessions), errors, len(files)))
    return sessions


"""
extract list of sessions from an activity file
"""
def extractSessions(filename, verbose=True):    
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
            if verbose:
                print (msg%row)
    
    return (sessions, excluded)


def isStartRow(row):
    return (len(row) > 3 and row[1] == 'start')

def isStopRow(row):
    return (len(row) > 1 and row[1] == 'stop')

def started(sess):
     return (sess.get('start') != None)
 
def startSession(row):
    sess = {'start': csvu.timeFromString(row[0]),
            'activity': row[2], 
            'posture': row[3] }
    if len(row) > 4:
        sess['notes'] = row[4]
    return sess
    
    
def stopSession(row, sess):
    sess['stop'] = csvu.timeFromString(row[0])
    sess['duration'] = csvu.duration(sess['start'], sess['stop'])
    return sess



if __name__ == '__main__':
    RAW_DATA_PATH = "C:\\Users\\julia\\Google Drive\\Academics\\Mestrado\\HeRV\\RawData\\0"
    sessions = parseActivityFiles(RAW_DATA_PATH, True)        
    print('first session:')
    print(sessions[0])
    
