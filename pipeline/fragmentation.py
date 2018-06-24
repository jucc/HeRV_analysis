import pandas as pd
import parseIntervalFiles as pif
import consolidateFiles as cf
import datacleaning as cl

from datetime import timedelta


def gen_fragments_dataset(sessions, duration, crop, mindata=0.83, maxpower=7500):  
    """
    breaks all sessions into fragments of 'duration' seconds after discarding
    'crop' seconds in the beginning of the session. Sessions that do not
    contain at least one full fragment according to these values are discarded
    """
    vsessions = cf.valid_sessions(sessions, crop+duration)
    print("%d valid sessions out of %d total (at least one full fragment of %d seconds after discarding first %d seconds)"
          %(len(vsessions), len(sessions), duration, crop))

    frags = []
    for sess in vsessions:
        frags.extend(fragment_session(sess, duration, crop, mindata))
    
    # clean dataset
    df = pd.DataFrame(frags)
    df = df[df['beatcount'] > mindata * duration]
    df = df[(df['hf'] < maxpower) & (df['lf'] < maxpower)]

    print(len(frags), 'total frags found and', len(df), 'kept')

    return df.drop(['rr'], axis = 1)


def fragment_session(sess, duration, crop, mindata=0.83):
    """
    breaks a session into fragments of 'duration' seconds after discarding
    'discard' seconds in the beginning of the session. Will return a list of frags, 
    which is empty if the session does not contain at least one full fragment 
    according to these values
    """
    f_id = 0
    frags = []
    fstop = sess['start'] + timedelta(seconds=crop)    
    while True:
        fstart = fstop
        fstop = fstart + timedelta(seconds=duration)
        if fstop > sess['stop']:
            break
        f = populate_fragment(sess, fstart, fstop, mindata * duration)
        f['f_id'] = f_id
        f_id = f_id +1
        frags.append(f)
    return frags


def populate_fragment(sess, fstart, fstop, minbeats):

    # fill basic info and intervals
    f = {'start':fstart, 'stop':fstop, 'user':sess['user'],
        'activity':sess['activity'], 'posture':sess['posture'], 'sess':sess['sess_id'],
        'rr': [x for x in sess['rr'] if x['date'] > fstart and x['date'] < fstop] }

    # clean intervals
    f['rr'] = cl.clean_rr_series(f['rr'])
    f['beatcount'] = len(f['rr'])

    # calculate aggregate features
    if f['beatcount'] > minbeats:
        f.update(cf.features_from_dic(f['rr']))
    
    return f