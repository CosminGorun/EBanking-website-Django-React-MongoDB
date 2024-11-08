
from django.shortcuts import render

from DataBase.Connection.MongoDBConnect import MongoDBConnect
from DataBase.DB_Data.ContBancar import ContBancar
from DataBase.DB_Data.User import User
from DataBase.DataBaseUC.TabelOperation import DataBaseTabel
from DataBase.EmailSender.Sender import EmailSender
from HtmlContent.ContextClass import LoginClientContext,CreateAccountContext
from random import randint, random

tabelaCont="ionut2"
dbCont="test1"

def generareIban():
    iban="RO"
    iban+=str(randint(100,999))
    iban+="SIM"
    iban+=str(randint(10**9,10**10-1))
    return iban


def goToCreateAccount(request):
    return render(request,'CreateAccount.html')

def generateCode():
    return randint(100000,999999)

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

    codeVerificare=generateCode()
    email=EmailSender()
    string="Codul este "
    string+=str(codeVerificare)
    email.sendMail(mail,"cod verificare",string)
    request.session['codeVerificare']=codeVerificare
    request.session['password']=password
    request.session['name']=name
    request.session['age']=age
    request.session['username']=username
    request.session['mail']=mail
    request.session['phoneNumber']=phoneNumber
    request.session['nextUserId']=nextUserId
    request.session['nextUserId']=nextUserId
    request.session['generareIban']=generareIban()
    return render(request,'ValidareMail.html', {'mail':mail})

def mailVerification(request):
    codeVer=request.session['codeVerificare']
    cod=request.POST.get('codVerificare')
    print(cod)
    print(codeVer)
    if cod==str(codeVer):
        name=request.session['name']
        age=request.session['age']
        username=request.session['username']
        mail=request.session['mail']
        phoneNumber=request.session['phoneNumber']
        password=request.session['password']
        nextUserId=int(request.session['nextUserId'])
        generareIban=request.session['generareIban']
        newUser = User(name, age, username, password, mail, phoneNumber, nextUserId)
        contBancar = ContBancar(nextUserId, 'RON', 0, generareIban)
        mongo = MongoDBConnect()
        tabel = DataBaseTabel(mongo.get_tabel("DB_User", "Users"))
        tabel.add(newUser)
        tabel= DataBaseTabel(mongo.get_tabel("DB_User", "conturi"))
        tabel.add(contBancar)
        return render(request,'Login.html')
    return render(request,'ValidareMail.html')
