import logging


def auth_api():
    token = input('Enter api token: ')
    secret = input('Enter secret key: ')
    return token, secret


def auth_db():
    address = input('Enter server address: ')
    login = input('Enter login: ')
    password = input('Enter password: ')
    return address, login, password
