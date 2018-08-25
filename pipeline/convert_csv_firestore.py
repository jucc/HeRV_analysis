import math
from datetime import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore

import parseIntervalFiles as pif
import parseActivityFiles as paf

hervdir = "C:\\Users\\Ju\\GDrive\\Projects\\HeRV\\"

## Firestore connection parameters

keyfile = hervdir + "Docs\\herv-3c5ea-firebase-adminsdk-99tjk-98193df3d9.json"
databaseURL = 'https://herv-3c5ea.firebaseio.com'

## CSV file reading parameters

source = hervdir + "Data\\Raw\\"
start_dt = datetime(2017, 10, 29)
end_dt = datetime(2018, 11, 1)


def u_ref(db, uid):
    return db.collection('users').document(str(uid))

def add_sessions(uid, start_dt, end_dt, source, dest):
    u_sess = paf.get_sessions(uid, start_dt, end_dt, source, verbose=False)
    print('adding', len(u_sess), 'sessions for user', uid)
    s_ref = u_ref(dest, uid).collection('sessions')
    for sess in u_sess:
        name = paf.csvu.string_from_time_filename(sess['start'])
        s_ref.document(name).set(sess)


def add_intervals(uid, start_dt, end_dt, source, dest):
    for day in pif.csvu.gendays(start_dt, end_dt):        
        add_day_intervals(uid, day, source, dest)
                

def add_day_intervals(uid, day, source, dest):    
    day_rr = pif.get_day_intervals(uid, day, source)    
    if len(day_rr) > 0:
        dayname = datetime.strftime(day, "%Y%m%d")
        print('adding', len(day_rr), 'RR intervals in', dayname)
        rr_ref = u_ref(dest, uid).collection('rr')
        rr_ref.document(dayname).set({'rr_count': len(day_rr)})
        mref = rr_ref.document(dayname).collection('minutes')
        for minutes in batch(group_by_minute(day_rr)):
            print ('adding batch with', len(minutes), 'minutes')
            gr = dest.batch()
            for (k, v) in minutes:
                doc = mref.document(k) 
                gr.set(doc, v)
            gr.commit()


def batch(d, n=500):
    x = len(d)
    l = list(d.items())
    for ndx in range(0, x, n):
        yield l[ndx:min(ndx + n, x)]
    

def group_by_minute(dayrr):
    d = {}
    #TODO obviously, this can be done without looping by splitting the list by h,m
    for h in range(24):
        for m in range(60):            
            mrr = [x for x in dayrr if x['date'].hour == h and x['date'].minute == m]
            if len(mrr) > 0:
                miname = str(str(h).zfill(2) + str(m).zfill(2))
                mi = {}
                for s in range(60):
                    srr = [x['interval'] for x in mrr if x['date'].second == s]
                    if len(srr) > 0:
                        mi[str(s)] = srr
                d[miname] = mi
    return d

## Initializing a client to communicate with Firestore

cred = credentials.Certificate(keyfile)
default_app = firebase_admin.initialize_app(cred, options={'databaseURL': databaseURL})
client = firestore.client()

print ("Connected to Firestore...")

## for each user id in the database, search for sessions and intervals in csvs

users = client.collection('users')

for doc in users.get():
    uid = int(doc.id)
    add_sessions(uid, start_dt, end_dt, source, client)
    add_intervals(uid, start_dt, end_dt, source, client)