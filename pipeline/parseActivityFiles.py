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
from os import path
import csvUtils as csvu


def get_files(user, dirname='.'):
    """
    returns all activity files for a given user
    """
    user_path = path.join(dirname, str(user))
    return list(csvu.getFilenames(user_path, r"^act.*"))


def get_user_sessions(user, dirname='.', verbose=True):
    """
    extract list of sessions from all activity files of a given user
    """
    sessions = []
    errors = 0
    for file in get_files(user, dirname):
        if verbose:
            print('reading %s ... '%file.split('\\')[-1])
        (f_sessions, f_errors) = extract_sessions(file, verbose)
        sessions.extend(f_sessions)
        errors += f_errors
    for sess in sessions:
        sess.update({"user": user})
    if verbose:
        print("%d sessions extracted and %d errors found"%(len(sessions), errors))
    return sessions


def extract_sessions(filename, verbose=True):
    """
    extract list of sessions from an activity file
    """
    sessions = []
    sess = {}
    excluded = 0
    reader = csvu.getFileReader(filename)
    for row in reader:

        if isStartRow(row) and not started(sess):
            sess = start_session(row)

        elif isStopRow(row) and started(sess):
            sessions.append(stop_session(row, sess))
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
                print(msg%row)

    return (sessions, excluded)


def isStartRow(row):
    return len(row) > 3 and row[1] == 'start'

def isStopRow(row):
    return len(row) > 1 and row[1] == 'stop'

def started(sess):
    return sess.get('start') != None

def start_session(row):
    sess = {'start': csvu.timeFromString(row[0]),
            'activity': row[2],
            'posture': row[3]}
    if len(row) > 4:
        sess['notes'] = row[4]
    return sess

def stop_session(row, sess):
    sess['stop'] = csvu.timeFromString(row[0])
    sess['duration'] = csvu.duration(sess['start'], sess['stop'])
    return sess