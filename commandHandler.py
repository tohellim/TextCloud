from User import User
from DBController import DBController


class commandHandler:
    def __init__(self):
        self.user = User()
        self.dbc = DBController()

    def handle(self, request):
        self.dbc.init_db()
        request = request.split(' ')
        command_list = ['reg', 'auth', 'create', 'update', 'delete', 'read', 'show', 'give_access', 'remove_access']
        if request[0] in command_list:
            if request[0] == 'reg':
                data = {
                    'login': '',
                    'password': ''
                }
                try:
                    data['login'] = request[1]
                except Exception:
                    return 'ERROR: BAD LOGIN'

                try:
                    data['password'] = request[2]
                except Exception:
                    return 'ERROR: BAD PASSWORD'

                response = self.dbc.add_user(data['login'], data['password'])

            if request[0] == 'create':
                data = {
                    'type': 'create',
                    'name': '',
                    'text': '',
                }
                try:
                    data['name'] = request[1]
                except Exception:
                    return 'ERROR: BAD TEXT NAME'

                try:
                    for i in range(2, len(request)):
                        data['text'] += (request[i]) + " "

                except Exception:
                    return 'ERROR: BAD TEXT'

                if (self.user.isActive == True):
                    response = self.dbc.add_file(data['name'], self.user.login, data['text'])
                else:
                    return ('Вы не авторизованы')

            if request[0] == 'auth':
                data = {
                    'login': '',
                    'password': ''
                }
                try:
                    data['login'] = request[1]
                except Exception:
                    return 'ERROR: BAD LOGIN'

                try:
                    data['password'] = request[2]
                except Exception:
                    return 'ERROR: BAD PASSWORD'

                self.user.set(data['login'], data['password'])
                self.user.isActive = True

                response = self.dbc.auth_user(data['login'], data['password'])

            if request[0] == 'read':
                data = {
                    'type': 'read',
                    'name': ''
                }
                try:
                    data['name'] = request[1]
                except Exception:
                    return 'ERROR: BAD TEXT NAME'

                if (self.user.isActive == True):
                    response = self.dbc.read_file(data['name'], self.user.login)
                else:
                    return ('Вы не авторизованы')

            if request[0] == 'update':
                data = {
                    'type': 'update',
                    'name': '',
                    'changed_text': ''
                }
                try:
                    data['name'] = request[1]
                except Exception:
                    return 'ERROR: BAD TEXT NAME'
                try:
                    for i in range(2, len(request)):
                        data['changed_text'] += (request[i]) + " "
                except Exception:
                    return 'ERROR: BAD TEXT VALUE'

                if (self.user.isActive == True):
                    response = self.dbc.update_file(data['name'], self.user.login, data['changed_text'])
                else:
                    return ('Вы не авторизованы')

            if request[0] == 'delete':
                data = {
                    'type': 'delete',
                    'name': ''
                }
                try:
                    data['name'] = request[1]
                except Exception:
                    return 'ERROR: BAD TEXT NAME'

                if(self.user.isActive == True):
                    response = self.dbc.delete_file(data['name'], self.user.login)
                else:
                    return ('Вы не авторизованы')

            if request[0] == 'show':
                if(self.user.isActive == True):
                    response = self.dbc.show_files(self.user.login)

            if request[0] == 'give_access':
                data = {
                    'name': '',
                    'user': '',
                    'access_type': ''
                }
                try:
                    data['name'] = request[1]
                except Exception:
                    return 'ERROR: BAD TEXT NAME'

                try:
                    data['user'] = request[2]
                except Exception:
                    return 'ERROR: BAD USERNAME'

                try:
                    if request[3] in ['read', 'update']:
                        data['access_type'] = request[3]
                    else:
                        return 'ERROR: BAD ACCESS TYPE'
                except Exception:
                    return 'ERROR: BAD ACCESS TYPE'

                if(self.user.isActive == True):
                    response = self.dbc.give_access(data['name'], self.user.login, data['access_type'], data['user'])
                else:
                    return ('Вы не авторизованы')

            if request[0] == 'remove_access':
                data = {
                    'name': '',
                    'user': '',
                    'access_type': ''
                }
                try:
                    data['name'] = request[1]
                except Exception:
                    return 'ERROR: BAD TEXT NAME'

                try:
                    data['user'] = request[2]
                except Exception:
                    return 'ERROR: BAD USERNAME'

                try:
                    data['access_type'] = request[3]
                except Exception:
                    return 'ERROR: BAD ACCESS TYPE'

                if(self.user.isActive == True):
                    response = self.dbc.remove_access(data['name'], self.user.login, data['access_type'], data['user'])
                else:
                    return ('Вы не авторизованы')

            self.dbc.close_db()
            if response is None:
                return 'Ошибка NoneType'
            else:
                return response
        else:
            return 'ERROR: BAD COMMAND'
