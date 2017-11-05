# -*- coding: utf-8 -*-

"""
uses parseIntervalFiles.py and parseAcrtivityFiles.py to read raw csv files and
generates consolidated files in formats  R and/or Kubios
"""

import parseIntervalFiles as pif
import parseActivityFiles as paf  
#pun intended :)
from datetime import datetime

"""
for each session read from activity files, adds the corresponding list of RR 
intervals contained in the time frame between its start and stop
"""
def getAllDataBySession(dirname, verbose=True):
    
    sessions = paf.parseActivityFiles(dirname, verbose)
    
    for sess in sessions:        
        sess['duration'] = int((sess['stop']-sess['start']).seconds)        
        sess['rr'] = pif.getIntervals(sess['start'], sess['stop'], dirname)        
        if verbose:
            printSession(sess)
            
    return sessions


def getValidSessions(sessions, min_len):
    return list(filter(lambda x: x['duration'] >= min_len and len(x['rr']) >= min_len, sessions))


def getInvalidSessions(sessions, min_len):
    return list(filter(lambda x: x['duration'] < min_len or len(x['rr']) < min_len, sessions))
                

def printSession(sess, forsheet=False, user=''):
    minutes = rrcount = 0
    if sess.get('duration'):
        minutes = sess['duration']/60
    if sess.get('rr'):
        rrcount = len(sess['rr'])    
    basicinfo = (minutes, rrcount)
    if forsheet:
        print("%s, %s, %s, "%(user,sess['activity'],sess['posture'])
              + str(sess['start']) + ", " + str(sess['stop'])
              + ", %d, %d"%basicinfo )
    else:
        print(str(sess['start']) + "\t%d min\t%d beats"%basicinfo)
        

def printSpreadsheetHeader():
    return " user, activity, posture, start, stop, duration, intervals"


def timeFromString(timestr):
    return datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    
    RAW_DATA_PATH = "C:\\Users\\julia\\Google Drive\\Academics\\Mestrado\\HeRV\\RawData\\0"
    data = getAllDataBySession(RAW_DATA_PATH, verbose=False)
    valid = getValidSessions(data, 300)
    invalid = getInvalidSessions(data, 300)
    print ("%d valid sessions out of of %d registered"%(len(valid), len(data)))
    print ("making sure: %d invalid sessions", len(invalid))
    #for sess in valid:
    #    printSession(sess, forsheet=True, user='0')
    for sess in invalid:
        printSession(sess, forsheet=False)
    
        