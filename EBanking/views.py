from lib2to3.fixes.fix_input import context

from django.http import HttpResponse
from django.shortcuts import render
from DataBase import *
from DataBase.Connection.MongoDBConnect import MongoDBConnect
from DataBase.DB_Data.Person import Person
from DataBase.DB_Data.User import User
from DataBase.DataBaseUC.TabelOperation import DataBaseTabel
from HtmlContent.loginClient import LoginClient


# Create your views here.
def mainPage(request):
    mongo=MongoDBConnect()
    tabel=DataBaseTabel(mongo.get_tabel("test1","ai"))
    listPers=tabel.getAll(Person)
    a1="eroare User"
    a2="er pass"
    return render(request, 'mainPage.html',{'listPers':listPers,'ErUserName':a1,'ErPassword':a2})

def addPers(request):
    mongo=MongoDBConnect()
    tabel=DataBaseTabel(mongo.get_tabel("test1","ionut1"))
    name = request.POST['namePerson']
    username = request.POST['agesPerson']
    password = request.POST['genderPerson']
    newPerson = User(name, username, password)
    tabel.add(newPerson)
    # tabel.delete({"name":name})
    # tabel.update({"name":name},{"name":"12","gender":"masculin"})
    # a=tabel.findAllBy({'ages':age})
    # for i in a:
    #     print(i['name'])
    return mainPage(request)

def loginClient(request):
    mongo = MongoDBConnect()
    tabel = DataBaseTabel(mongo.get_tabel("test1", "ionut1"))
    username = request.POST.get('username')
    password = request.POST.get('password')
    context=LoginClient()
    user=tabel.findOneBy({"username":username})
    if user is None:
        context.setUserNameEr("eroare user")
        return render(request, 'Login.html', {'context':context})
    else:
        if user['parola'] != password:
            context.setUserPasswordEr("eroare password")
            return render(request, 'Login.html', {'context':context})
    return mainPage(request)
