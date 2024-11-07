# datele se salveaza in baza de date DB_User in colectia conturi
class ContBancar:
    __fields__ = ['userID', 'moneda','sold','iban']
    def __init__(self,userID,moneda,sold,iban):
        self.userID = userID
        self.moneda = moneda
        self.sold = sold
        self.iban = iban
    def toDic(self):
        return {"userID": self.userID,"moneda":self.moneda, "sold": self.sold, "iban": self.iban}