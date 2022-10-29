from datetime import datetime
import os
import stat

def lasted_access(user_email: str):
    """Gera um arquivo .txt com a data e hora de quando foi feita a validação do e-mail

    Args:
        user_email (str): e-mail de referencia que sera usado para gerar o arquivo .txt
    """
    #* Verifica se o arquivo existe
    if os.path.isfile(f"{user_email}.txt"):
        # Modifica a permissão do arquivo para leitura, escrita e execução
        os.chmod("exemplo.txt", stat.S_IRWXU)

    #* Abre o arquivo para escrita
    arquivo = open(f"{user_email}.txt", 'w')

    #* Escreve no arquivo
    exection_time = datetime.now()
    date_time = exection_time.strftime("%d/%m/%Y, %H:%M:%S")
    arquivo.write(f"Ultimo acesso: {user_email} - {date_time}")

    #* Fecha o arquivo
    arquivo.close()

    #* Modifica o arquivo apenas para leitura
    os.chmod(f"{user_email}.txt", stat.S_IRUSR)
