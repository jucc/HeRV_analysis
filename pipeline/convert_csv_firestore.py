import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore

from datetime import datetime

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


def add_sessions(uid, start_dt, end_dt, source, dest):
    u_sess = paf.get_sessions(uid, start_dt, end_dt, source, verbose=False)
    print('adding', len(u_sess), 'sessions for user', uid)
    s_ref = dest.document(str(uid)).collection('sessions')
    for sess in u_sess:
        name = paf.csvu.string_from_time_filename(sess['start'])
        s_ref.document(name).set(sess)
    print ('sessions added to firestore...')


def add_intervals(uid, start_dt, end_dt, source, dest):
    rr_ref = dest.document(str(uid)).collection('rr')
    for day in pif.csvu.gendays(start_dt, end_dt):
        day_rr = pif.get_day_intervals(uid, day, source)
        if len(day_rr) > 0:
            add_day_intervals(day, day_rr, rr_ref)
    print ('intervals added to firestore')


def add_day_intervals(day, day_rr, dest):
    dayname = datetime.strftime(day, "%Y%m%d")
    dest.document(dayname).set({'rr_count': len(day_rr)})    
    print(len(day_rr), 'RR intervals to add in', dayname)
    for h in range(0,24):
        hour_rr = [x for x in day_rr if x['date'].hour == h] #obviously, break this better bc its an ordered seq
        if len(hour_rr) > 0:
            href = dest.document(dayname).collection('minutes')
            add_hour_intervals(h, hour_rr, href)


def add_hour_intervals(h, rr, dest):    
    print(h , ': ', len(rr))
    for min in range(60):
        miname = str(str(h).zfill(2) + str(min).zfill(2))
        m = []
        for s in range(60):            
            srr = [x['interval'] for x in rr if x['date'].minute == min and x['date'].second == s]
            if len(srr) > 0:
                m.append({str(s): srr})
        if len(m) > 0:
            dest.document(miname).set({'intervals': m})


## Initializing a client to communicate with Firestore

cred = credentials.Certificate(keyfile)
default_app = firebase_admin.initialize_app(cred, options={'databaseURL': databaseURL})
client = firestore.client()

print ("Connected to Firestore...")

## for each user id in the database, search for sessions and intervals in csvs

u_ref = client.collection('users')

for doc in u_ref.get():
    uid = int(doc.id)
    add_sessions(uid, start_dt, end_dt, source, u_ref)
    add_intervals(uid, start_dt, end_dt, source, u_ref)