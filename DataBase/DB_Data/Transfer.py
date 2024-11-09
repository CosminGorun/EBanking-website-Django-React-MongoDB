# datele se salveaza in baza de date Tranzacti in colectia transfer

class Transfer:
    __fields__ = ['IDTransfer', 'IBANtrimite', 'IBANprimeste','sumaTransfer','moneda','dataTranzactiei','finalizat']
    def __init__(self, IDTransfer, IBANtrimite, IBANprimeste, sumaTransfer, moneda, dataTranzactiei, finalizat):
        self.IDTransfer = IDTransfer
        self.IBANtrimite = IBANtrimite
        self.IBANprimeste = IBANprimeste
        self.sumaTransfer = sumaTransfer
        self.moneda = moneda
        self.dataTranzactiei = dataTranzactiei
        self.finalizat = finalizat

    def toDic(self):
        return {
            "IDTransfer": self.IDTransfer,
            "IBANtrimite": self.IBANtrimite,
            "IBANprimeste": self.IBANprimeste,
            "sumaTransfer": self.sumaTransfer,
            "moneda": self.moneda,
            "dataTranzactiei": self.dataTranzactiei,
            "finalizat": self.finalizat
        }
