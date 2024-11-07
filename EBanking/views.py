from lib2to3.fixes.fix_input import context

from django.http import HttpResponse
from django.shortcuts import render
from DataBase import *
from DataBase.Connection.MongoDBConnect import MongoDBConnect
from DataBase.DB_Data.ContBancar import ContBancar
from DataBase.DB_Data.Person import Person
from DataBase.DB_Data.User import User
from DataBase.DataBaseUC.TabelOperation import DataBaseTabel
from HtmlContent.ContextClass import LoginClientContext,CreateAccountContext
from random import randint
tabelaCont="ionut2"
dbCont="test1"
def generareIban():
    iban="RO"
    iban+=str(randint(100,999))
    iban+="SIM"
    iban+=str(randint(10**9,10**10-1))
    return iban
# Create your views here.
def mainPage(request,user,cont):
    mongo=MongoDBConnect()
    tabel=DataBaseTabel(mongo.get_tabel("test1","ai"))
    listPers=tabel.getAll(Person)
    a1="eroare User"
    a2="er pass"
    return render(request, 'mainPage.html',{'listPers':listPers,'ErUserName':a1,'ErPassword':a2,'USER' : user,'CONT': cont})

def addPers(request):
    mongo=MongoDBConnect()
    tabel=DataBaseTabel(mongo.get_tabel("test1","ionut1"))
    name = request.POST['namePerson']
    age=request.POST['agePerson']
    username = request.POST['usernamePerson']
    password = request.POST['genderPerson']
    mail=request.POST['mailPerson']
    phoneNumber=request.POST['phoneNumber']

    listUser=tabel.getAll(User)
    nextUserId=1
    for usr in listUser:
        if usr.userID>nextUserId:
            nextUserId=usr.userID
    nextUserId+=1
    newPerson = User(name,age, username, password,mail,phoneNumber,nextUserId)
    tabel.add(newPerson)
    # tabel.delete({"name":name})
    # tabel.update({"name":name},{"name":"12","gender":"masculin"})
    # a=tabel.findAllBy({'ages':age})
    # for i in a:
    #     print(i['name'])
    #return mainPage(request,newPerson)
def transferConturi(request):
    mongo = MongoDBConnect()
    tabel = DataBaseTabel(mongo.get_tabel("DB_User", "Users"))
    tabelCont=DataBaseTabel(mongo.get_tabel(dbCont,tabelaCont))
    ibanSursa=request.POST.get('ibanSursa')
    ibanDestinatie=request.POST.get('ibanDestinatie')
    suma=int(request.POST.get('suma'))
    val=request.POST.get('userID')
    user=tabel.findOneBy({"userID":int(val)})
    cont=tabelCont.findOneBy({"iban":ibanSursa})
    contDest=tabelCont.findOneBy({"iban":ibanDestinatie})
    if contDest is None:
        return mainPage(request,user,cont)#cont gresit (nu am mai adugat html, urmeaza)

    #nu am adaugat verificari pt testare
    contDest2=contDest.copy()
    cont2=cont.copy()
    contDest2["sold"]=str(int(contDest["sold"])+suma)#soldul trb facut int UPS :(
    cont2['sold']=str(int(cont['sold'])-suma)
    tabelCont.updateOne(cont,cont2)
    tabelCont.updateOne(contDest, contDest2)
    #urmeaza sa adaug si in tabela de transfer
    return mainPage(request,user,cont2)
def goToLoginClient(request):
    return render(request, 'Login.html')
def loginClient(request):
    mongo = MongoDBConnect()
    tabel = DataBaseTabel(mongo.get_tabel("DB_User", "Users"))
    tabelCont = DataBaseTabel(mongo.get_tabel(dbCont, tabelaCont))
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
    cont = tabelCont.findOneBy({"userID": user['userID']}) # daca s-a validat user-ul inseamna ca are si userId :D asa ca nu verific nimic
    return mainPage(request,user,cont)

def goToCreateAccount(request):
    return render(request,'CreateAccount.html')

def createAccount(request):
    context=CreateAccountContext()
    mongo = MongoDBConnect()
    tabel = DataBaseTabel(mongo.get_tabel("DB_User", "Users"))
    tabelCont=DataBaseTabel(mongo.get_tabel(dbCont,tabelaCont))
    listUser=tabel.getAll(User)

    # for i in listUser:
    #     tabel.deleteOne({"username":i.username})
    # return
    name = request.POST.get('name')
    if len(name)<3:
        context.ErName="Numele este prea scurt!"
        return render(request, 'CreateAccount.html', {'context':context})
    if any(c in name for c in '[]{},._;:\|!@#$%^&*()-_=+|~=:<>?'):
        context.ErName = "Numele nu poate contine caractere speciale!"
        return render(request, 'CreateAccount.html', {'context':context})

    age = int(request.POST.get('age'))
    if age<18:
        context.ErAge="Varsta trebuie sa fie mai mare de 18 ani!!!!!!!"
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

    nextUserId=0
    for usr in listUser:
        if usr.userID>nextUserId:
            nextUserId=usr.userID
    nextUserId+=1

    tabel.add(User(name,age, username, password,mail,phoneNumber,nextUserId))
    tabelCont.add(ContBancar(nextUserId,'RON',0,generareIban()))
    return render(request,'Login.html')

