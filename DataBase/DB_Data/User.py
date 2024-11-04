class User:
    __fields__ = ['name', 'username', 'password']
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

