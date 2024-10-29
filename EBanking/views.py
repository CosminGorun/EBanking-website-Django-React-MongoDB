from django.http import HttpResponse
from django.shortcuts import render
from DataBase import *
from DataBase.Connection.DB_Connect import connect, getTabel
from DataBase.DB_Data.Person import Person
from DataBase.DataBaseUC.DB_Operation import addPerson, getAllPerson


# Create your views here.
def mainPage(request):
    client=connect()
    if client==None:
        print("Connection Error")
    else:
        print("Connected")
        tabel=getTabel(client,"test1","ai")
        listPers=getAllPerson(tabel)
    return render(request, 'mainPage.html',{'listPers':listPers})

def addPers(request):
    client = connect()
    if client == None:
        print("Connection Error")
    else:
        print("Connected")
        tabel = getTabel(client, "test1", "ai")
        name = request.POST['namePerson']
        age = request.POST['agesPerson']
        gender = request.POST['genderPerson']
        newPerson = Person(name, age, gender)
        addPerson(tabel,newPerson)
        print("Person added")
    return mainPage(request)
