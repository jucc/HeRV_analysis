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
    print(uid, ' - sessions:', len(u_sess))
    
    s_ref = dest.document(str(uid)).collection('sessions')
    for sess in u_sess:
        s_ref.document().set(sess)

    print ('sessions added to firestore...')


def add_intervals(uid, start_dt, end_dt, source, dest):
    rr_ref = dest.document(str(uid)).collection('rr')
    for day in pif.csvu.gendays(start_dt, end_dt):
        day_rr = pif.get_day_intervals(uid, day, source)
        if len(day_rr) > 0:
            add_day_intervals(day, day_rr, rr_ref)


def add_day_intervals(day, day_rr, dest):
    dayname = datetime.strftime(day, "%Y%m%d")
    day_ref = dest.document(dayname)
    print('creating rr collection for day ', dayname, 'with len ', len(day_rr))
    #     batch_op = client.batch()
    for h in range(0,24):
        hour_ref = day_ref.collection(str(h))
        hour_rr = [x for x in day_rr if x['date'].hour == h]
        if len(hour_rr) > 0:
            print(h, len(hour_rr))            
            for rr in hour_rr:    
                name = str(rr['date'].minute).zfill(2) + str(rr['date'].second).zfill(2)
                #hour_ref.document(name).set(rr['interval'])
                print(name, rr['interval'])

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