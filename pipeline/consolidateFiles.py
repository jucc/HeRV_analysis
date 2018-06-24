# -*- coding: utf-8 -*-

"""
uses parseIntervalFiles.py and parseAcrtivityFiles.py to read raw csv files and
generates consolidated files in formats  R and/or Kubios
"""
from datetime import timedelta, datetime, date
import numpy as np
from hrv.classical import time_domain, frequency_domain
from os import path

import csvUtils as csvu
import parseIntervalFiles as pif
import parseActivityFiles as paf
#pun intended :)


def get_user_sessions(user, start_dt, end_dt, dirname='.', verbose=True):
    """
    extract list of sessions from all activity files of a given user
    (only the session descriptions, not the intervals)
    """
    sessions = []
    errors = 0
    for day in pif.gendays(start_dt, end_dt):
        file = paf.get_day_file(user, day, dirname)        
        if file:
            if verbose:
                print('reading %s ... '%file.split('\\')[-1])
            (f_sessions, f_errors) = paf.extract_sessions(file, verbose)
            sessions.extend(f_sessions)
            errors += f_errors
    for sess in sessions:
        sess.update({"user": user})
    if verbose:
        print("%d sessions extracted and %d errors found"%(len(sessions), errors))
    return sessions


def sessions_add_beats(sessions, dirname, verbose=True):
    """
    for each session, the list of RR intervals between its start and stop
    is added to its attributes
    * Not a pure function, will alter the sessions input parameter * 
    """

    for sess in sessions:
        sess['duration'] = int((sess['stop']-sess['start']).seconds)
        sess['rr'] = pif.get_intervals(sess['user'], sess['start'], sess['stop'], dirname)
        if verbose:
            print(print_summary(sess))

    return sessions


def valid_sessions(sessions, min_len):
    """
    filters only sessions with at least min_len
    """
    return [sess for sess in sessions if sess['duration'] >= min_len]


def beatlist(beats):
    """
    converts the list of intervals (dic with datetime and value) to an array of interval values
    """
    return np.array([x['interval'] for x in beats])


def features_from_list(rrlist):
    """
    calculates time and frequency domain features from a list of RR interval values (no timestamp)
    """
    td = time_domain(rrlist)
    fd = frequency_domain(rrlist)
    td.update(fd)
    return td


def features_from_dic(beats):
    """
    calculates time and frequency domain features from a dic of beats (timestamp + RR interval value)
    """ 
    return features_from_list(beatlist(beats))


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
