# -*- coding: utf-8 -*-

"""
uses parseIntervalFiles.py and parseAcrtivityFiles.py to read raw csv files and
generates consolidated files in formats  R and/or Kubios
"""
from datetime import timedelta
import numpy as np
from hrv.classical import time_domain, frequency_domain
from os import path

import csvUtils as csvu
import parseIntervalFiles as pif
import parseActivityFiles as paf
#pun intended :)


def sessions_add_beats(sessions, dirname, verbose=True):
    """
    for each session, the list of RR intervals between its start and stop
    is added to its attributes
    * Not a pure function, will alter the sessions input parameter * 
    """

    for sess in sessions:
        sess['duration'] = int((sess['stop']-sess['start']).seconds)
        sess['rr'] = pif.get_intervals(sess['start'], sess['stop'], dirname)
        if verbose:
            print(print_summary(sess))

    return sessions


def valid_sessions(sessions, min_len):
    """
    filters only sessions with at least min_len
    """
    return [sess for sess in sessions if sess['duration'] >= min_len]


def fragment_sessions(sessions, duration=300, discard=90):
    """
    breaks all sessions into fragments of 'duration' seconds after discarding
    'discard' seconds in the beginning of the session. Sessions that do not
    contain at least one full fragment according to these values are discarded
    """
    vsessions = valid_sessions(sessions, discard+duration)
    print("%d valid sessions out of %d total (at least one full fragment of %d seconds after discarding first %d seconds)"
          %(len(vsessions), len(sessions), duration, discard))

    frags = []
    for sess in vsessions:
        frags.extend(frags_session(sess, discard, duration))
    return frags


def frags_session(sess, discard, duration):
    """
    breaks a session into fragments of 'duration' seconds after discarding
    'discard' seconds in the beginning of the session. Will return a list of frags, 
    which is empty if the session does not contain at least one full fragment 
    according to these values
    """
    f_id = 0
    frags = []
    fstop = sess['start'] + timedelta(seconds=discard)
    while True:
        fstart = fstop
        fstop = fstart + timedelta(seconds=duration)
        if fstop > sess['stop']:
            break
        frags.append({'start':fstart, 'stop':fstop, 
                      'activity':sess['activity'], 'posture':sess['posture'],
                      'user':sess['user'],
                      'sess':sess['sess_id'], 'order':f_id})
        f_id = f_id +1

    return frags

        
def beats_in_fragment(frag, dirname='.'):
    """
    lists RR intervals recorded in the duration of the fragment (in the form of dics
    with datetime and value)
    """
    return pif.get_intervals(frag['start'], frag['stop'], path.join(dirname, str(frag['user'])))


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
    features = ['mrr', ]
    return td


def features_from_dic(beats):
    """
    calculates time and frequency domain features from a dic of beats (timestamp + RR interval value)
    """ 
    return features_from_list(beatlist(beats))


def aggregate_data(frag, dirname):
    """
    add time domain and frequency domain metrics for the beats in the fragment
    """

    agg = frag
    agg.update(features_from_dic(beats_in_fragment(frag, dirname)))
    return agg


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
