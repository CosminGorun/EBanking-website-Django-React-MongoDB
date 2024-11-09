from django.shortcuts import render
from DataBase.Connection.MongoDBConnect import MongoDBConnect
from DataBase.DB_Data.Person import Person
from DataBase.DB_Data.Transfer import Transfer
from DataBase.DataBaseUC.TabelOperation import DataBaseTabel

tabelaTr="ionut3"
dbTr="test1"

def mainPage(request,user,cont,context=None):
    mongo=MongoDBConnect()
    tabel=DataBaseTabel(mongo.get_tabel("test1","ai"))
    tabelTr = DataBaseTabel(mongo.get_tabel(dbTr, tabelaTr))
    # listPers=tabel.getAll(Person)
    listTr=tabelTr.getAll(Transfer)
    tranzactiiUserOUT=[]
    tranzactiiUserIN = []
    print(cont["iban"])
    for tranzactie in listTr:
        if tranzactie.IBANprimeste==cont["iban"] and tranzactie.finalizat==0:
            tranzactiiUserOUT.append(tranzactie)
        if tranzactie.IBANtrimite==cont["iban"] and tranzactie.finalizat==0:
            tranzactiiUserIN.append(tranzactie)
    if context is not None:
        err=context
    else:
        err=""
    a1="eroare User"
    a2="er pass"
    return render(request, 'mainPage.html',{'listTransferOUT':tranzactiiUserOUT,'listTransferIN':tranzactiiUserIN,'ErUserName':a1,'ErPassword':a2,'err':err,'USER' : user,'CONT': cont})
