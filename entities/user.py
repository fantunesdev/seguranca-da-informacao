class User:
    def __init__(self, email, password, verified, token, menu_response):
        self.__email = email
        self.__password = password
        self.__verified = verified
        self.token = token
        self.__menu_response = menu_response

    def __repr__(self):
        return self.__email

    @property
    def email(self):
        return self.__email

    @property
    def password(self):
        return self.__password

    def set_credentials(self):
        self.__email = input('Digite seu e-mail: ')
        self.__password = input('Digite a sua senha (deve ter no mínimo 6 caracteres): ')

    def is_credentials_valid(self):
        if self.token:
            return True
        return False

    @property
    def verified(self):
        return self.__verified

    @verified.setter
    def verified(self, value):
        self.__verified = value

    def is_verified(self):
        return self.__verified

    @property
    def menu_response(self):
        return self.__menu_response

    def set_menu_response(self):
        self.__menu_response = int(input('Selecione uma das opções acima: '))
