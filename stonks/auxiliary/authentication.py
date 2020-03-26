from IPython import get_ipython
from IPython.display import clear_output


def is_notebook():
    try:
        shell = get_ipython().__class__.__name__
        return shell == 'ZMQInteractiveShell'
    except NameError:
        return False


# Запрос пароля для api Binance
def auth_api(level='READ'):
    if level == 'READ':
        return 'distonx', 'nevermind'
    else:
        token = input('Enter api token: ')
        secret = input('Enter secret key: ')

        if is_notebook():
            clear_output()

        return token, secret


# Запрос пароля для базы данных
def auth_db():
    address = input('Enter server address: ')
    login = input('Enter login: ')
    password = input('Enter password: ')

    if is_notebook():
        clear_output()

    return address, login, password
