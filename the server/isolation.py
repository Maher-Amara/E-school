import pickle


def access(user_name, user_password):
    with open('data base.maher', 'rb') as fic:
        ClientsIDs = pickle.load(fic)
    user_name = user_name.strip()
    exists = False
    for client in ClientsIDs:
        if user_name.strip() == client['user name']:
            if user_password == client['password']:
                return True, 'access granted'
            else:
                return False, 'wrong password'
        else:
            return False, 'wrong user name'


while True:
    user_name = input('user name: ')
    user_password = input('password: ')
    access_var = access(user_name, user_password)
    print(access_var)
    print(type(access_var))
