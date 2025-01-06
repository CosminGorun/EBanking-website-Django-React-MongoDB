# datele se salveaza in baza de date DB_User in colectia Users
class User:
    __fields__ = ['name', 'username', 'password','mail','phoneNumber','userID','age']
    def __init__(self, name,age, username, password,mail, phoneNumber, userID):
        self.name = name
        self.age = age
        self.username = username
        self.password = password
        self.mail = mail
        self.phoneNumber =  phoneNumber
        self.userID = userID
    def toDic(self):
        return {"name": self.name,"age":self.age, "username": self.username, "password": self.password, "mail": self.mail, "phoneNumber": self.phoneNumber , "userID": self.userID}
    def getMail(self):
        return self.mail