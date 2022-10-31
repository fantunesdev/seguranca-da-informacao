import os
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_second_factor_authentication_email(user):
    """
    Envia o e-mail para se realizar o segundo fator de autentificação.
    :param user: instância do objeto User
    :return: retorna o integer randômico gerado
    """
    print(f'Um e-mail com o código de confirmacao está sendo enviado para {user}...')
    server = "smtp.gmail.com"  # Seta a URL do servidor SMTP
    port = 587  # Seta a porta
    username = os.environ['EMAIL']  # Seta o username através da variável de ambiente
    password = os.environ['APP_PASSWORD']  # Seta a senha da aplicação através da variável de ambiente.
    secret = random.randint(100, 1000)  # Gera um integer randômico de 3 dígitos.
    mail_body = f'Código de validação: {secret}.'  # Seta o corpo da mensagem com o integer gerado.

    mail_message = MIMEMultipart()  # Instancia um objeto com as configurações de mensagem do MIME Multipart
    mail_message['From'] = username  # Seta o e-mail remetente.
    mail_message['To'] = user.email  # Seta o e-mail destinatário.
    mail_message['Subject'] = 'Código e-mail'  # Seta o título do e-mail.
    mail_message.attach(MIMEText(mail_body, 'plain'))  # Adiciona o corpo da mensagem no email.

    connection = smtplib.SMTP(server, port)  # Conecta com o servidor SMTP
    connection.starttls()  # Configura a conexão SMTP no modo TLS
    connection.login(username, password)  # Autentica no servidor SMTP
    connection.send_message(mail_message)  # Envia o e-mail
    connection.quit()  # Encerra a conexão
    return secret
