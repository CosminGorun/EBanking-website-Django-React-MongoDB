from django.shortcuts import render
from DataBase.Connection.MongoDBConnect import MongoDBConnect
from DataBase.DB_Data.Person import Person
from DataBase.DataBaseUC.TabelOperation import DataBaseTabel

def mainPage(request,user,cont):
    mongo=MongoDBConnect()
    tabel=DataBaseTabel(mongo.get_tabel("test1","ai"))
    listPers=tabel.getAll(Person)
    a1="eroare User"
    a2="er pass"
    return render(request, 'mainPage.html',{'listPers':listPers,'ErUserName':a1,'ErPassword':a2,'USER' : user,'CONT': cont})
