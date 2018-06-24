# -*- coding: utf-8 -*-

"""
Raads activity files and extracts sessions from them
ACTIVITY FILE STRUCTURE (two events):
datetime,start,activity-category,posture
datetime,stop,,
SESSION STRUCTURE:
datetime-start,datetime-end,activity-name,posture,notes
"""
from os import path
import csvUtils as csvu
from datetime import datetime


def get_all_files(user, dirname='.'):
    """
    returns all activity files for a given user
    """
    user_path = path.join(dirname, str(user))
    return list(csvu.get_filenames(user_path, r"^act.*"))


def get_day_file(user, dt, dirname='.'):
    """
    returns the activity file for a given user in a given day
    """
    user_path = path.join(dirname, str(user))
    filepattern = datetime.strftime(dt, '%y%m%d')
    regexp = r"^act%s" % (filepattern)
    filelist = list(csvu.get_filenames(user_path, regexp))
    if len(filelist) > 0:
        return filelist[0]
    else:
        return None


def extract_sessions(filename, verbose=True):
    """
    extract list of sessions from an activity file
    """
    sessions = []
    sess = {}
    excluded = 0
    reader = csvu.get_rows(filename)
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

## HELPER FUNCTIONS (only relevant in this context)

def isStartRow(row):
    return len(row) > 3 and row[1] == 'start'

def isStopRow(row):
    return len(row) > 1 and row[1] == 'stop'

def started(sess):
    return sess.get('start') != None

def start_session(row):
    sess = {'start': csvu.time_from_string(row[0]),
            'activity': row[2],
            'posture': row[3]}
    if len(row) > 4:
        sess['notes'] = row[4]
    return sess

def stop_session(row, sess):
    sess['stop'] = csvu.time_from_string(row[0])
    sess['duration'] = csvu.duration(sess['start'], sess['stop'])
    return sess