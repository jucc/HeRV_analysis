import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore

from datetime import datetime

import parseIntervalFiles as pif
import parseActivityFiles as paf

## Firestore connection parameters

keyfile = "C:\\Users\\Ju\\GDrive\\Projects\\HeRV\\Docs\\herv-3c5ea-firebase-adminsdk-99tjk-98193df3d9.json"
databaseURL = 'https://herv-3c5ea.firebaseio.com'

## CSV file reading parameters

source = "C:\\Users\\Ju\\GDrive\\Projects\\HeRV\\Data\\Raw\\"
start_dt = datetime(2017, 10, 29)
end_dt = datetime(2017, 11, 1)

## Initializing a client to communicate with Firestore
cred = credentials.Certificate(keyfile)
default_app = firebase_admin.initialize_app(cred, options={'databaseURL': databaseURL})
client = firestore.client()

## Add users --------------------------------------------------------------------------------

# users = {
#     '0': {'age':34, 'weight':80, 'height':'150', 'gender': 'F'},
#     '1': {'age':32, 'weight':65, 'height':'171', 'gender': 'M'},
#     '2': {'age':31, 'weight':70, 'height':'170', 'gender': 'M'},
#     '3': {'age':27, 'weight':90, 'height':'160', 'gender': 'M'},
#     '4': {'age':51, 'weight':80, 'height':'155', 'gender': 'F'},
#     '5': {'age':53, 'weight':80, 'height':'165', 'gender': 'F'},
#     '6': {'age':17, 'weight':80, 'height':'175', 'gender': 'M'},
#     '7': {'age':84, 'weight':40, 'height':'145', 'gender': 'F'}
# }

u_ref = client.collection('users')

# for k, v in users.items():
#     u_ref.document(k).set(v)

## print all documents in the users collection
# users = u_ref.get()
# for doc in users:
#     print(u'Document data: {}'.format(doc.to_dict()))

## Add sessions -----------------------------------------------------------------------------

# s_ref = client.collection('sessions')

# for user in range(0,8):
#     u_sess = paf.get_user_sessions(user, dirname=source, verbose=False)
#     print(user, ' sessions:', len(u_sess))
#     for sess in u_sess:
#         s_ref.document().set(sess)

## Add intervals -----------------------------------------------------------------------------

for user in range(0,8):
    uu_ref = u_ref.document(str(user))
    dirname = source+'\\'+str(user)    
    print(u'Document data: {}'.format(uu_ref.get().to_dict()))
    rr_ref = uu_ref.collection('rr')
    for day in pif.gendays(start_dt, end_dt):        
        docname = datetime.strftime(day, "%Y%m%d")        
        day_rr = pif.get_day_intervals(day.year, day.month, day.day, dirname)
        if len(day_rr) > 0:
            print(docname, len(day_rr))
            day_ref = rr_ref.document(docname)            
            for h in range(0,24):
                hour_rr = [x for x in day_rr if x['date'].hour == h]
                if len(hour_rr) > 0:
                    print(h, len(hour_rr))
                    day_ref.collection(str(h))
        #     batch_op = client.batch()
        #     for rr in u_rr:
        #         doc = rr_ref.document()
        #         rr_ref.document().set(rr)