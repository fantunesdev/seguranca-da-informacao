import os

import pyrebase

from dotenv import load_dotenv

load_dotenv()

firebase_config = {
    'apiKey': os.environ['API_KEY'],
    'authDomain': os.environ['AUTH_DOMAIN'],
    'projectId': os.environ['PROJECT_ID'],
    'databaseURL': os.environ['DATABASE_URL'],
    'storageBucket': os.environ['STORAGE_BUCKET'],
    'messagingSenderId': os.environ['MESSAGING_SENDER_ID'],
    'appId': os.environ['APP_ID'],
    'measurementId': os.environ['MEASUREMENT_ID']
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

user = input('Digite seu e-mail: ')
password = input('Digite a sua senha: ')

response = auth.sign_in_with_email_and_password(user, password)

print(auth.get_account_info(response['idToken']))
