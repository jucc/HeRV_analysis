# -*- coding: utf-8 -*-

"""
uses parseIntervalFiles.py and parseAcrtivityFiles.py to read raw csv files and
generates consolidated files in formats  R and/or Kubios
"""
import numpy as np
import pandas as pd
from datetime import timedelta, datetime, date
from hrv.classical import time_domain, frequency_domain
from os import path

import csvUtils as csvu
import parseIntervalFiles as pif
import parseActivityFiles as paf
import datacleaning as cl
#pun intended :)


def gen_sessions_dataset(users, start_dt, end_dt, minrr=300, maxrr=1800, dirname='.', verbose=True):
    """
    generates a full session dataset, with cleaned up rr intervals and features
    params
    users: list of user ids to filter on. If empty, includes all users    
    start_dt, end_dt: range of dates to include in the dataset
    minrr, maxrr: acceptable range of RR intervals (intervals outiside the range are discarded)
    """
    ds = []
    discarded = 0
    id = 0
    for user in users:
        usessions = paf.get_sessions(user, start_dt, end_dt, dirname, verbose)
        for sess in usessions:
            if (verbose):
                print('[',user,']', sess['activity'], sess['start'])
            sess['user'] = user
            sess = extract_sess_data(sess, minrr, maxrr, dirname)
            if sess['beatscount'] > sess['duration'] * 0.5:
                sess['sess_id'] = id
                id = id+1
                ds.append(sess)
            else:
                discarded = discarded + 1
    if verbose:
        print (len(ds), 'sessions completed and', discarded, 'discarded for lack of RR data')
    return ds


def extract_sess_data(sess, minrr=300, maxrr=1800, dirname='.'):
    """
    adds interval and aggregate data to the session
    TODO refactor separation of concerns
    """
    rr = pif.get_intervals(sess['user'], sess['start'], sess['stop'], dirname)
    beats = len(rr)
    rr = cl.clean_rr_series(rr, minrr, maxrr)
    sess['rr'] = rr    
    sess['beatscount'] = len(rr)     
    sess['removed_artifacts'] = beats - sess['beatscount']
    sess['duration'] = int((sess['stop']-sess['start']).seconds)    
    if (sess['beatscount'] > 10):
        sess.update(features_from_list(beatlist(rr)))
    return sess
    

def beatlist(beats):
    """
    converts the list of intervals (dic with datetime and value) to an array of interval values
    """
    return np.array([x['interval'] for x in beats])


def features_from_list(rrlist):
    """
    calcu
    lates time and frequency domain features from a list of RR interval values (no timestamp)
    """
    td = time_domain(rrlist)
    fd = frequency_domain(rrlist)
    td.update(fd)
    return td


def print_summary(sess, forsheet=False, user=''):
    """
    print session summary formatted for csv file if forsheet=True0 or console output otherwise
    """
    minutes = rrcount = 0
    if sess.get('duration'):
        minutes = sess['duration']/60
    if sess.get('rr'):
        rrcount = len(sess['rr'])
    basicinfo = (minutes, rrcount)
    if forsheet:
        return "%s, %s, %s, %s, %s"%(user, sess['activity'], sess['posture'], str(sess['start']), str(sess['stop'])) + ", %d, %d"%basicinfo
    else:
        return str(sess['start']) + "\t%d min\t%d beats"%basicinfo


def print_header():
    """
    print header for session summary csv file containing
    """
    return "user, activity, posture, start, stop, duration, intervals"
