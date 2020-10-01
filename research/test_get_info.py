def get_access_info():
    with open('../settings/access_info.txt') as file:
        access_dict = eval(file.read())
    return access_dict


print(get_access_info())
