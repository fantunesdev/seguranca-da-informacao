import os

import pyrebase
from dotenv import load_dotenv

import system_messages

load_dotenv()


class FirebaseRepository:
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

    def create_user(self, user):
        print('Criando usuário...')
        self.auth.create_user_with_email_and_password(user.email, user.password)
        system_messages.print_success_message(f'E-mail {user.email} cadastrado com sucesso!')

    def validate_credentials(self, user):
        response = self.auth.sign_in_with_email_and_password(user.email, user.password)
        user.token = response['idToken']
        self.verify_email(user)
        print(f'Você está usando as credenciais do e-mail {user.email}')
        return response

    def send_verification(self, user):
        self.verify_email(user)
        if user.is_verified():
            system_messages.print_success_message('O e-mail já foi verificado anteriormente.')
        else:
            self.auth.send_email_verification(user.token)
            message = f'E-mail de verificação enviado para {user}. Se não encontrar, verifique na caixa de SPAM.'
            system_messages.print_success_message(message)

    def verify_email(self, user):
        info = self.auth.get_account_info(user.token)
        users = info['users']
        user.verified = users[0]['emailVerified']

