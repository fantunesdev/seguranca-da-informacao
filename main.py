import json
import requests.exceptions

from repositories import firebase_repository, smtp_repository, os_repository
from entities.user import User
import system_messages

user = User(
    email=None,
    password=None,
    verified=False,
    is_authenticated=False,
    token=None,
    menu_response=None
)

# Instancia a classe com as funções de conexão com o Firebase
repository_firebase = firebase_repository.FirebaseRepository()

while True:
    system_messages.print_menu()  # Printa as opções de menu
    try:  # Envolve o código num try-except para tratar os erros
        user.set_menu_response()  # Pega a escolha de menu do usuário
        # Verfica a resposta do usuário e realiza a ação escolhida
        if user.menu_response == 1:  # Opção de criar usuário
            user.set_credentials()
            repository_firebase.create_user(user)
        elif user.menu_response == 2:  # Opção de enviar e-mail de verificação
            user.set_credentials()
            repository_firebase.validate_credentials(user)
            repository_firebase.send_verification(user)  # Envia o e-mail de verificação.
        elif user.menu_response == 3:  # Opção de realizar login com autenticação múltipo fator
            user.set_credentials()
            repository_firebase.validate_credentials(user)
            repository_firebase.verify_email(user)
            if user.is_verified():  # Checa se o e-mail já foi verificado
                print(f'Primeira etapa realizada com sucesso.')
                print('Iniciando segundo fator de autentificação.')
                secret = smtp_repository.send_second_factor_authentication_email(user)  # gera o secret, envia por email
                try:
                    # Lê a partir do teclado o código de verificação enviado por e-mail
                    verification_code = int(input(f'Digite o código de verificação enviado para o e-mail {user}: '))
                    if secret == verification_code:  # Verifica se o código digitado pelo usuário confere com o secret
                        user.is_authenticated = True
                        system_messages.print_success_message('Login realizado com sucesso')
                    else:
                        system_messages.print_error_message('Código inválido. Tente novamente.')
                except ValueError:
                    system_messages.print_error_message('Você não digitou um número. Por favor, tente novamente!')
            else:
                # Impede a tentativa de login se o e-mail ainda não foi verificado, conforme requisito solicitado.
                message = f'O e-mail {user} ainda não foi verificado. \n' \
                          f'Por favor, faça a verificação e tente novamente.'
                system_messages.print_error_message(message)
        elif user.menu_response == 4:  # Opção para manipulação de arquivos
            # Verifica se a autenticação em múltiplos fatores foi realizada
            if user.credentials_are_valid() and user.is_authenticated:
                os_repository.lasted_access(user.email)  # Altera o arquivo
            else:
                system_messages.print_error_message('É necessário realizar o login antes de continuar.')
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
