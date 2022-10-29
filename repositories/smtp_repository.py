import os
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_second_factor_authentication_email(user):
    print(f'Um e-mail com o código de confirmacao está sendo enviado para {user}...')
    server = "smtp.gmail.com"
    port = 587
    username = os.environ['EMAIL']
    password = os.environ['APP_PASSWORD']
    secret = random.randint(100, 1000)
    mail_body = f'Código de validação: {secret}.'

    mail_message = MIMEMultipart()
    mail_message['From'] = username
    mail_message['To'] = user.email
    mail_message['Subject'] = 'Código e-mail'
    mail_message.attach(MIMEText(mail_body, 'plain'))

    connection = smtplib.SMTP(server, port)
    connection.starttls()
    connection.login(username, password)
    connection.send_message(mail_message)
    connection.quit()
    return secret
