import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore



keyfile = "C:\\Users\\Ju\\GDrive\\Projects\\HeRV\\Docs\\herv-3c5ea-firebase-adminsdk-99tjk-98193df3d9.json"
databaseURL = 'https://herv-3c5ea.firebaseio.com'

# initializing a client to communicate
cred = credentials.Certificate(keyfile)
default_app = firebase_admin.initialize_app(cred, options={'databaseURL': databaseURL})
client = firestore.client()

# print all documents in the users collection
u_ref = client.collection('users')
users = u_ref.get()
for doc in users:
    print(u'Document data: {}'.format(doc.to_dict()))