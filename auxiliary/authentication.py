import logging


def auth_api():
    logging.info('Authentication of api')
    token = input('Enter api token: ')
    secret = input('Enter secret key: ')
    return token, secret


def auth_db():
    logging.info('Authentication of database')
    address = input('Enter server address: ')
    login = input('Enter login: ')
    password = input('Enter password: ')
    return address, login, password
