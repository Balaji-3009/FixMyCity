import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("fixmycity-11f7f-firebase-adminsdk-fbsvc-cae2c778cc.json")
firebase_admin.initialize_app(cred)
