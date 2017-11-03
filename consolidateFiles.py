# -*- coding: utf-8 -*-

"""
uses parseIntervalFiles.py and parseAcrtivityFiles.py to read raw csv files and
generates consolidated files in formats  R and/or Kubios
"""

import parseIntervalFiles as pif
import parseActivityFiles as paf  
#pun intended :)
from datetime import datetime

MIN_SESS = 300

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
            print (sess['start'], sess['stop'])
            minutes = sess['duration']/60
            rrcount = len(sess['rr'])
            print("duration: %d min, rr: %d, avg bpm: %d"%(minutes, rrcount, rrcount/minutes))
            
    valid_sess = list(filter(lambda x: x['duration'] > MIN_SESS and len(x['rr']) > MIN_SESS, sessions))
    print ("%d valid sessions out of %d sessions registered"
           %(len(valid_sess), len(sessions)))
                

def timeFromString(timestr):
    return datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S")

if __name__ == '__main__':
    
    RAW_DATA_PATH = "C:\\Users\\julia\\Google Drive\\Academics\\Mestrado\\HeRV\\RawData\\0"
    data = getAllDataBySession(RAW_DATA_PATH)
        