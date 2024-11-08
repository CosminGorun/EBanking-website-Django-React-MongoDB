
from django.shortcuts import render

from DataBase.Connection.MongoDBConnect import MongoDBConnect
from DataBase.DB_Data.ContBancar import ContBancar
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