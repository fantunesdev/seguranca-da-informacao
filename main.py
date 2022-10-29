import json
import requests.exceptions

from repositories import firebase_repository, smtp_repository
from entities.user import User
import system_messages

user = User(
    email=None,
    password=None,
    verified=False,
    token=None,
    menu_response=None
)

repository_firebase = firebase_repository.FirebaseRepository()

while True:
    system_messages.print_menu()
    try:
        user.set_menu_response()
        if user.menu_response == 1:
            user.set_credentials()
            repository_firebase.create_user(user)
        elif user.menu_response == 2:
            if user.is_credentials_valid():
                repository_firebase.send_verification(user)
            else:
                system_messages.print_error_message('Suas credenciais não são válidas. '
                                                    'Entre com seus dados e tente novamente.')
                user.set_credentials()
                repository_firebase.validate_credentials(user)
        elif user.menu_response == 3:
            if user.is_credentials_valid():
                repository_firebase.verify_email(user)
                if user.is_verified():
                    print('Segundo fator de autentificação.')
                    secret = smtp_repository.send_second_factor_authentication_email(user)
                    try:
                        verification_code = int(input(f'Digite o código de verificação enviado para o e-mail {user}: '))
                        if secret == verification_code:
                            message = 'Email verificado com sucesso! \nObrigado por usar nosso sistema! Volte sempre!'
                            system_messages.print_success_message(message)
                            break
                        else:
                            system_messages.print_error_message('Código inválido. Tente novamente.')
                    except ValueError:
                        system_messages.print_error_message('Você não digitou um número. Por favor, tente novamente!')
                else:
                    message = f'O e-mail {user} ainda não foi verificado. \n' \
                              f'Por favor, faça a verificação e tente novamente.'
                    system_messages.print_error_message(message)
            else:
                system_messages.print_error_message('Você não está logado, entre com as credenciais e tente novamente.')
                user.set_credentials()
                repository_firebase.validate_credentials(user)
        elif user.menu_response == 4:
            print(f'Usuário: {user.email}\n'
                  f'Password: {user.password}\n'
                  f'Verified: {user.verified}\n'
                  f'Is verified: {user.is_verified()}\n'
                  f'Token: {user.token}\n')
        elif user.menu_response == 9:
            system_messages.print_success_message('Obrigado por usar nosso sistema! Volte sempre!')
            break
        else:
            raise ValueError

    except ValueError:
        system_messages.print_error_message('Você não digitou uma opção válida. Por favor, tente novamente!')

    except requests.exceptions.HTTPError as HTTPError:
        response = json.loads(HTTPError.strerror)
        error_message = response['error']['message']

        if 'EMAIL_EXISTS' in error_message:
            system_messages.print_error_message('O e-mail já foi cadastrado anteriormente. Por favor, tente novamente.')
        elif 'INVALID_EMAIL' in error_message:
            system_messages.print_error_message('Vocẽ não parece ter digitado um endereço de e-mail.Tente novamente.')
        elif 'MISSING_PASSWORD' in error_message:
            system_messages.print_error_message('Você esqueceu de digitar uma senha. Por favor, tente novamente.')
        elif 'WEAK_PASSWORD' in error_message:
            system_messages.print_error_message('A senha precisa ter pelo menos 6 caracteres. '
                                                'Por favor, tente novamente.')
        elif 'INVALID_PASSWORD' in error_message:
            system_messages.print_error_message('Você forneceu credenciais incorretas. Por favor, tente novamente.')
        elif 'EMAIL_NOT_FOUND' in error_message:
            system_messages.print_error_message('O e-mail não foi encontrado em nosso banco de dados. '
                                                'Por favor, tente novamente.')
        else:
            system_messages.print_error_message(error_message)
