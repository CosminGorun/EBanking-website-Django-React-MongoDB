class User:
    __fields__ = ['name', 'username', 'parola']
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.parola = password

    def toDic(self):
        return {"name": self.name, "username": self.username, "parola": self.parola}
