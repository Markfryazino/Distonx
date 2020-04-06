from IPython import get_ipython
from IPython.display import clear_output
from stonks.DataCatcher import DB


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
    if DB.authorized:
        return DB.credentials
    else:
        address = input('Enter server address: ')
        login = input('Enter login: ')
        password = input('Enter password: ')
        DB.authorized = True
        DB.credentials = (address, login, password)

    if is_notebook():
        clear_output()

    return address, login, password
