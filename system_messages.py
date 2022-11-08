from colorama import Fore, Style


def print_menu():
    """
    Printa na tela as opções de menu
    """
    print('#' * 30)
    print('#' * 3 + ' ' * 10 + '\033[1m' + 'MENU' + '\033[0m' + ' ' * 10 + '#' * 3)
    print('#' * 30)
    print()
    print('1 - Cadastrar usuário.')
    print('2 - Verificar e-mail.')
    print('3 - Login com autenticação multi-fator.')
    print('4 - Manipular arquivo e permissões')
    print('9 - Encerrar.')
    print()


def print_success_message(message):
    """
    Printa na tela as mensagens de sucesso na cor verde.
    :param message: mensagem a ser printada
    """
    print(Fore.GREEN + '\033[1m')
    print(message)
    print('\033[0m' + Style.RESET_ALL)


def print_error_message(message):
    """
    Printa na tela as mensagens de erro na cor vermelha.
    :param message: mensagem a ser printada
    """
    print(Fore.RED + '\033[1m')
    print(f'*** ATENÇÃO!!! *** {message}')
    print(Style.RESET_ALL + '\033[0m')