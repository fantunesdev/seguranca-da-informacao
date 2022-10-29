import json
import os
import random
import smtplib

import pyrebase
import requests.exceptions

from dotenv import load_dotenv
from colorama import Fore, Style
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

while True:
    print('#' * 30)
    print('#' * 3 + ' ' * 10 + '\033[1m' + 'MENU' + '\033[0m' + ' ' * 10 + '#' * 3)
    print('#' * 30)
    print()
    print('1 - Cadastrar usuário.')
    print('2 - Verificar e-mail.')
    print('3 - Autenticar Usuário.')
    print('9 - Encerrar.')
    print()

    try:
        user_response = int(input('Selecione uma das opções acima: '))

        if user_response == 1:
            user = input('Digite seu e-mail: ')
            password = input('Digite a sua senha: ')
            response = auth.create_user_with_email_and_password(user, password)
            print(Fore.GREEN + '\033[1m')
            print(f'E-mail {user} cadastrado com sucesso.')
            print('\033[0m' + Style.RESET_ALL)
        elif user_response == 2:
            user = input('Digite seu e-mail: ')
            password = input('Digite a sua senha: ')
            response = auth.sign_in_with_email_and_password(user, password)
            id_token = response['idToken']
            auth.send_email_verification(id_token)
            print(Fore.GREEN + '\033[1m')
            print(f'E-mail de verificação enviado para {user}. Se não encontrar, verifique na caixa de SPAM.')
            print(Style.RESET_ALL + '\033[0m')
        elif user_response == 3:
            user = input('Digite seu e-mail: ')
            password = input('Digite a sua senha: ')
            response = auth.sign_in_with_email_and_password(user, password)
            id_token = response['idToken']
            info = auth.get_account_info(id_token)
            users = info['users']
            email_is_verify = users[0]['emailVerified']

            if email_is_verify:
                print('Segundo fator de autentificação.')
                server = "smtp.gmail.com"
                port = 587
                username = os.environ['EMAIL']
                password = os.environ['APP_PASSWORD']
                secret = random.randint(100, 1000)
                mail_body = f'Código de validação: {secret}.'

                message = MIMEMultipart()
                message['From'] = username
                message['To'] = user
                message['Subject'] = 'Código e-mail'
                message.attach(MIMEText(mail_body, 'plain'))

                connection = smtplib.SMTP(server, port)
                connection.starttls()
                connection.login(username, password)
                connection.send_message(message)
                connection.quit()

                try:
                    verification_code = int(input(f'Digite o código de verificação enviado para o e-mail {user}: '))

                    if secret == verification_code:
                        print(Fore.GREEN + '\033[1m')
                        print('Email verificado com sucesso')
                        print('Obrigado por usar nosso sistema! Volte sempre!')
                        print('\033[0m' + Style.RESET_ALL)
                        break
                    else:
                        print(Fore.RED + '\033[1m')
                        print('Código inválido. Tente novamente.')
                        print('\033[0m' + Style.RESET_ALL)
                except ValueError:
                    print(Fore.RED + '\033[1m')
                    print('*** ATENÇÃO!! Você não digitou um número. Por favor, tente novamente ***')
                    print(Style.RESET_ALL + '\033[0m')
            else:
                print(Fore.RED + '\033[1m' + 'ATENÇÃO!!')
                print(f'*** O e-mail {user} ainda não foi verificado. '
                      f'Por favor, faça a verificação e tente novamente. ***')
                print(Style.RESET_ALL + '\033[0m')
        elif user_response == 9:
            print()
            print('Obrigado por usar nosso sistema! Volte sempre!')
            break
        else:
            raise ValueError

    except ValueError:
        print(Fore.RED + '\033[1m')
        print('*** ATENÇÃO!! Você não digitou um número. Por favor selecione uma das opções válidas. ***')
        print(Style.RESET_ALL + '\033[0m')

    except requests.exceptions.HTTPError as HTTPError:
        response = json.loads(HTTPError.strerror)
        error_message = response['error']['message']

        print(Fore.RED + '\033[1m')

        if error_message == 'EMAIL_EXISTS':
            print('*** ATENÇÃO!! O e-mail já foi cadastrado anteriormente. Por favor, tente novamente. ***')
        elif error_message == 'MISSING_PASSWORD':
            print('*** ATENÇÃO!! Você esqueceu de digitar uma senha. Por favor, tente novamente. ***')
        elif error_message == 'WEAK_PASSWORD : Password should be at least 6 characters':
            print(f'*** ATENÇÃO!! A senha precisa ter pelo menos 6 caracteres. Por favor, tente novamente. ***')
        elif error_message == 'INVALID_PASSWORD':
            print('*** ATENÇÃO!! Os dados de login estão incorretos. Por favor, tente novamente. ***')
        elif error_message == 'EMAIL_NOT_FOUND':
            print('*** ATENÇÃO!! O e-mail não foi encontrado em nosso banco de dados. Por favor, tente novamente. ***')
        else:
            print(error_message)

        print(Style.RESET_ALL + '\033[0m')

