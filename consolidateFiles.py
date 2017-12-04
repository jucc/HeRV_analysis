# -*- coding: utf-8 -*-

"""
uses parseIntervalFiles.py and parseAcrtivityFiles.py to read raw csv files and
generates consolidated files in formats  R and/or Kubios
"""

import csvUtils as csvu
import parseIntervalFiles as pif
import parseActivityFiles as paf  
#pun intended :)

from datetime import timedelta


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
            print(sessPrint(sess))
            
    return sessions


def getValidSessions(sessions, min_len):
    return [sess for sess in sessions if sess['duration'] >= min_len and len(sess['rr']) >= min_len]


def fragment_sessions(sessions, duration=300, discard=90):
    
    vsessions = getValidSessions(sessions, discard+duration)
    print ("%d valid sessions out of %d total (at least one full fragment of %d seconds after discarding first %d seconds)"
           %(len(vsessions), len(sessions), duration, discard))

    s_id = 0

    frags = []
    for sess in vsessions:
        f_id = 0   
        fstop = sess['start'] + timedelta(seconds=discard)
        while True:
            fstart = fstop
            fstop = fstart + timedelta(seconds=duration)
            if fstop > sess['stop']:
                break
            rr = pif.getIntervals(fstart, fstop, dirname=RAW_DATA_PATH)
            frags.append({ 'start': fstart, 'stop': fstop, 'rr':rr, 'activity': sess['activity'], 'sess': s_id, 'order': f_id })
            f_id = f_id +1

        s_id = s_id + 1
        
    return frags           


def sessPrint(sess, forsheet=False, user=''):
    minutes = rrcount = 0
    if sess.get('duration'):
        minutes = sess['duration']/60
    if sess.get('rr'):
        rrcount = len(sess['rr'])    
    basicinfo = (minutes, rrcount)
    if forsheet:
        return("%s, %s, %s, "%(user,sess['activity'],sess['posture'])
              + str(sess['start']) + ", " + str(sess['stop'])
              + ", %d, %d"%basicinfo )
    else:
        return(str(sess['start']) + "\t%d min\t%d beats"%basicinfo)
        

def sessHeaderPrint():
    return "user, activity, posture, start, stop, duration, intervals"




if __name__ == '__main__':
    
    user = 0
    RAW_DATA_PATH = "C:\\Users\\julia\\Google Drive\\Academics\\Mestrado\\HeRV\\Data\\Raw\\%d"%user
    PRE_DATA_PATH = "C:\\Users\\julia\\Google Drive\\Academics\\Mestrado\\HeRV\\Data\\PreProcessed\\%d"%user
    
    data = getAllDataBySession(RAW_DATA_PATH, verbose=False)
    valid = getValidSessions(data, 300)    
    print ("%d valid sessions out of of %d registered"%(len(valid), len(data)))
    
    slist = open(PRE_DATA_PATH + '\\sessions.csv', 'w')
    slist.write(sessHeaderPrint()+'\n')
    for sess in valid:
        slist.write(sessPrint(sess, forsheet=True, user=user)+'\n')
        rrfilename = '%s\\%s-%s.csv'%(PRE_DATA_PATH, sess['activity'], csvu.stringFromTimeFilename(sess['start']))        
        rrf = open(rrfilename, 'w')
        for rr in sess['rr']:            
            #rrf.write("%s, %d\n"%(stringFromTimeKubios(rr['date']), int(rr['interval'])))
            rrf.write("%d\n"%(int(rr['interval'])))
        rrf.close()
    slist.close()      