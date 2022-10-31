import os

import pyrebase
from dotenv import load_dotenv

import system_messages

load_dotenv()  # Lê as variáveis de ambiente do arquivo ".env"


class FirebaseRepository:
    # Cria um dicionário com as constantes fornecidas pelo Firebase para autentificação da aplicação.
    # Obs: Por questões de segurança, as variáveis são setadas no arquivo ".env"
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
    # Inicializa o app com as constantes fornecidas
    firebase = pyrebase.initialize_app(firebase_config)

    # Autentica a aplicação.
    auth = firebase.auth()

    def create_user(self, user):
        """
        Cria uma conta no Firebase.
        :param user: instância do objeto User
        """
        print('Criando usuário...')
        self.auth.create_user_with_email_and_password(user.email, user.password)  # Cria a conta no Firebase
        system_messages.print_success_message(f'E-mail {user.email} cadastrado com sucesso!')

    def validate_credentials(self, user):
        """
        Realiza a primeira etapa do login, verificando e-mail e senha. Atribui ao objeto User o token criptografado com
        as informações do usuário logado no Firebase.
        :param user: instância do objeto User
        :return: resposta do Firebase.
        """
        response = self.auth.sign_in_with_email_and_password(user.email, user.password)  # guarda a resposta da conexão
        user.token = response['idToken']  # Seta o atributo token da instância User
        self.verify_email(user)  # Checa se o e-mail já foi verificado
        return response

    def send_verification(self, user):
        """
        Envia a mensagem de verificação de e-mail.
        :param user: instância do objeto User
        :return:
        """
        self.verify_email(user)

        # Checa se o e-mail já foi verificado anteriormente. Se não foi, envia o e-mail de verificação.
        if user.is_verified():
            system_messages.print_success_message('O e-mail já foi verificado anteriormente.')
        else:
            self.auth.send_email_verification(user.token)  # Envia o e-mail de verificação
            message = f'E-mail de verificação enviado para {user}. Se não encontrar, verifique na caixa de SPAM.'
            system_messages.print_success_message(message)

    def verify_email(self, user):
        """
        Checa no Firebase se o e-mail já foi verificado e atribui a resposta ao atributo verified do objeto User.
        :param user: instância do objeto User
        """
        info = self.auth.get_account_info(user.token)  # Pega a info da conta logada no Firebase atraves do id token
        users = info['users']
        user.verified = users[0]['emailVerified']  # Guarda o estatus de verificação no atributo verified do objeto User
