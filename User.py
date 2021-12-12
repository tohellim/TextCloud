class User:
    global login
    global password
    global isActive

    def __init__(self):
        self.isActive = False

    def set(self, logs, passz):
        self.login = logs
        self.password = passz
