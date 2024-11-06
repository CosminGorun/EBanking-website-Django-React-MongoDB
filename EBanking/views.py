from lib2to3.fixes.fix_input import context

from django.http import HttpResponse
from django.shortcuts import render
from DataBase import *
from DataBase.Connection.MongoDBConnect import MongoDBConnect
from DataBase.DB_Data.Person import Person
from DataBase.DB_Data.User import User
from DataBase.DataBaseUC.TabelOperation import DataBaseTabel
from HtmlContent.ContextClass import LoginClientContext,CreateAccountContext


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
        context.ErUserName="User-ul nu a fost gasit!"
        return render(request, 'Login.html', {'context':context})
    else:
        if user['password'] != password:
            context.ErPassword="Parola gresita!"
            return render(request, 'Login.html', {'context':context})
    return mainPage(request,user)

def goToCreateAccount(request):
    return render(request,'CreateAccount.html')

def createAccount(request):
    context=CreateAccountContext()
    mongo = MongoDBConnect()
    tabel = DataBaseTabel(mongo.get_tabel("DB_User", "Users"))

    name = request.POST.get('name')
    if len(name)<3:
        context.ErName="Numele este prea scurt!"
        return render(request, 'CreateAccount.html', {'context':context})
    if any(c in name for c in '[]{},._;:\|!@#$%^&*()-_=+|~=:<>?'):
        context.ErName = "Numele nu poate contine caractere speciale!"
        return render(request, 'CreateAccount.html', {'context':context})

    username = request.POST.get('username')
    if len(username)<5:
        context.ErUserName="Username-ul este prea scurt!"
        return render(request, 'CreateAccount.html', {'context':context})
    if tabel.findOneBy({"username":username}) :
        context.ErUserName="Acest username exista!"
        return render(request, 'CreateAccount.html', {'context':context})

    password = request.POST.get('password')
    if len(password)<8:
        context.ErPassword="Parola trebuie sa contina minim 8 caractere!"
        return render(request, 'CreateAccount.html', {'context':context})

    mail=request.POST.get('mail')
    # if not validEmail(mail):
    #     context.ErEmail="Email invalid!"
    #     return render(request, 'CreateAccount.html', {'context':context})

    phoneNumber=request.POST.get('phoneNumber')
    if len(phoneNumber)!=10:
        context.ErPhoneNumber="numar gresit!"
        return render(request, 'CreateAccount.html', {'context':context})

    tabel.add(User(name, username, password, mail, phoneNumber))
    return render(request,'Login.html')

