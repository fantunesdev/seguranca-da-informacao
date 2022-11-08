from datetime import datetime
import os
import stat


def lasted_access(user_email: str):
    """
    Manipula um arquivo ".txt" com a data e hora de quando foi feita a validação do e-mail.
    :param user_email: e-mail de referencia que sera usado para gerar o arquivo ".txt"
    """

    # * Verifica se o arquivo existe
    if os.path.isfile(f"historico-{user_email}.txt"):
        print(f'O arquivo historico-{user_email}.txt já existe. Atribuindo permissões de escrita.')
        os.chmod(f"historico-{user_email}.txt", stat.S_IRWXU)  # Modifica a permissão do arquivo para leitura, escrita e execução

    # * Abre o arquivo para escrita
    with open(f'historico-{user_email}.txt', 'a', encoding='utf-8') as archive:
        execution_time = datetime.now()
        date_time = execution_time.strftime('%d/%m/%Y %H:%M:%S')
        archive.write(f'Último acesso: {user_email} - {date_time}\n')
        archive.close()
        print('Salvando arquivo.')

    # * Modifica o arquivo apenas para leitura
    print('Atribuindo apenas permissão de leitura.')
    os.chmod(f"historico-{user_email}.txt", stat.S_IRUSR)
