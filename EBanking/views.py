from lib2to3.fixes.fix_input import context

from django.http import HttpResponse
from django.shortcuts import render
from DataBase import *
from DataBase.Connection.MongoDBConnect import MongoDBConnect
from DataBase.DB_Data.Person import Person
from DataBase.DB_Data.User import User
from DataBase.DataBaseUC.TabelOperation import DataBaseTabel
from HtmlContent.loginClient import LoginClientContext


# Create your views here.
def mainPage(request,user):
    mongo=MongoDBConnect()
    tabel=DataBaseTabel(mongo.get_tabel("test1","ai"))
    listPers=tabel.getAll(Person)
    a1="eroare User"
    a2="er pass"
    return render(request, 'mainPage.html',{'listPers':listPers,'ErUserName':a1,'ErPassword':a2,'USER' : user})

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

def goToLoginClient(request):
    return render(request, 'Login.html')
def loginClient(request):
    mongo = MongoDBConnect()
    tabel = DataBaseTabel(mongo.get_tabel("DB_User", "Users"))
    username = request.POST.get('username')
    password = request.POST.get('password')
    context=LoginClientContext()
    user=tabel.findOneBy({"username":username})
    if user is None:
        context.setUserNameEr("eroare user")
        return render(request, 'Login.html', {'context':context})
    else:
        if user['password'] != password:
            context.setUserPasswordEr("eroare password")
            return render(request, 'Login.html', {'context':context})
    return mainPage(request,user)

def goToCreateAccount(request):
    return render(request,'CreateAccount.html')

def createAccount(request):
    name = request.POST.get('name')
    username = request.POST.get('username')
    password = request.POST.get('password')
    mail=request.POST.get('mail')
    phoneNumber=request.POST.get('phoneNumber')
    mongo=MongoDBConnect()
    tabel = DataBaseTabel(mongo.get_tabel("DB_User", "Users"))
    tabel.add(User(name, username, password, mail, phoneNumber))
    return render(request,'Login.html')