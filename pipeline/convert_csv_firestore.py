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

# insert users

u_ref = client.collection('users')

u_ref.document(u'0').set({
    u'age': 34,
    u'gender': u'F',
    u'height': 150,
    u'weight': 80
})

u_ref.document(u'1').set({
    u'age': 32,
    u'gender': u'M',
    u'height': 171,
    u'weight': 66
})

u_ref.document(u'2').set({
    u'age': 31,
    u'gender': u'M',
    u'height': 170,
    u'weight': 70
})


# print all documents in the users collection
users = u_ref.get()
for doc in users:
    print(u'Document data: {}'.format(doc.to_dict()))
