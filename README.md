## Projeto de Segurança da Tecnologia da Informação

1) Solicitar que o usuário digite suas credencias (email e senha);
2) Criar previamente as credencias no Firebase;
3) Autenticar o usuário no Firebase;
   * Antes de autenticar o usuário deve estar com o e-mail obrigatoriamente verificado;
   * Caso o email não esteja verificado não realizar a autenticação;
   * Quando o email já estiver verificado, autenticar o usuário no Firebase;
4) Após autenticar no Firebase vamos criar o mecanismo de controle de acesso;

    * Criar um arquivo texto pelo Python (arquivo “acesso.txt”);
    * Certificar que o arquivo “acesso.txt” já existe, caso já tenha sido criado você deve fornecer permissões de leitura, escrita e execução para o proprietário do arquivo.
    * Abrir o arquivo “acesso.txt” para escrita;
    * Fornecer as informações do último acesso do usuário (email, data e hora);
    * Fechar o arquivo “acesso.txt”;
    * Modificar as permissões do arquivo, deixar o arquivo apenas com permissão de leitura.