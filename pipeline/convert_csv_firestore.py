import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore

import parseIntervalFiles as pif
import parseActivityFiles as paf


keyfile = "C:\\Users\\Ju\\GDrive\\Projects\\HeRV\\Docs\\herv-3c5ea-firebase-adminsdk-99tjk-98193df3d9.json"
databaseURL = 'https://herv-3c5ea.firebaseio.com'

source = "C:\\Users\\Ju\\GDrive\\Projects\\HeRV\\Data\\Raw\\"

# initializing a client to communicate
cred = credentials.Certificate(keyfile)
default_app = firebase_admin.initialize_app(cred, options={'databaseURL': databaseURL})
client = firestore.client()

# add users --------------------------------------------------------------------------------

users = {
    '0': {'age':34, 'weight':80, 'height':'150', 'gender': 'F'},
    '1': {'age':32, 'weight':65, 'height':'171', 'gender': 'M'},
    '2': {'age':31, 'weight':70, 'height':'170', 'gender': 'M'},
    '3': {'age':27, 'weight':90, 'height':'160', 'gender': 'M'},
    '4': {'age':51, 'weight':80, 'height':'155', 'gender': 'F'},
    '5': {'age':53, 'weight':80, 'height':'165', 'gender': 'F'},
    '6': {'age':17, 'weight':80, 'height':'175', 'gender': 'M'},
    '7': {'age':84, 'weight':40, 'height':'145', 'gender': 'F'}
}

u_ref = client.collection('users')

for k, v in users.items():
    u_ref.document(k).set(v)

# print all documents in the users collection
users = u_ref.get()
for doc in users:
    print(u'Document data: {}'.format(doc.to_dict()))

# add sessions -----------------------------------------------------------------------------

u_ref = client.collection('sessions')

for user in range(0,8):
    u_sess = paf.get_user_sessions(user, dirname=source, verbose=False)
    print(user, ':', len(u_sess))
    for sess in u_sess:
        u_ref.document().set(sess)