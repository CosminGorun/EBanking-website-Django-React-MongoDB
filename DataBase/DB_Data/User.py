# datele se salveaza in baza de date DB_User in colectia Users
class User:
    __fields__ = ['name', 'username', 'password','mail','phoneNumber','userID']
    def __init__(self, name, username, password,mail, phoneNumber):
        self.name = name
        self.username = username
        self.password = password
        self.mail = mail
        self.phoneNumber =  phoneNumber

    def toDic(self):
        return {"name": self.name, "username": self.username, "password": self.password, "mail": self.mail, "phoneNumber": self.phoneNumber}
