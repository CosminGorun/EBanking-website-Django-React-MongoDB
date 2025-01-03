
from django.shortcuts import render

from DataBase.Connection.MongoDBConnect import MongoDBConnect
from DataBase.DB_Data.ContBancar import ContBancar
from DataBase.DB_Data.User import User
from DataBase.DataBaseUC.TabelOperation import DataBaseTabel
from DataBase.EmailSender.Sender import EmailSender
from HtmlContent.ContextClass import LoginClientContext,CreateAccountContext
from random import randint, random
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

tabelaCont = "conturi"
dbCont = "DB_User"


def generareIban(moneda):
    iban = moneda
    iban += str(randint(100, 999))
    iban += "SIG"
    iban += str(randint(10 ** 9, 10 ** 10 - 1))
    return iban


@csrf_exempt
def goToCreateAccount(request):
    return render(request, 'CreateAccount.html')


def generateCode():
    return randint(100000, 999999)


@csrf_exempt
def createAccount(request):
    try:
        body = json.loads(request.body)
        name = body.get('name')
        mail = body.get('mail')
        phoneNumber = body.get('phoneNumber')
        password = body.get('password')
        age = body.get('age')
        username = body.get('username')

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

    context = CreateAccountContext()
    mongo = MongoDBConnect()
    tabel = DataBaseTabel(mongo.get_tabel("DB_User", "Users"))
    tabelCont = DataBaseTabel(mongo.get_tabel(dbCont, tabelaCont))
    listUser = tabel.getAll(User)

    # for i in listUser:
    #     tabel.deleteOne({"username":i.username})
    # return
    nextUserId = 0
    for usr in listUser:
        if usr.userID > nextUserId:
            nextUserId = usr.userID
    nextUserId += 1

    codeVerificare = generateCode()
    email = EmailSender()
    string = "Codul este "
    string += str(codeVerificare)
    email.sendMail(mail, "cod verificare", string)
    print(codeVerificare)
    request.session['codeVerificare'] = codeVerificare
    request.session['password'] = password
    request.session['name'] = name
    request.session['age'] = age
    request.session['username'] = username
    request.session['mail'] = mail
    request.session['phoneNumber'] = phoneNumber
    request.session['nextUserId'] = nextUserId
    request.session['nextUserId'] = nextUserId
    request.session['generareIban'] = generareIban("RO")

    return JsonResponse({
        'message': 'Account created successfully. Please check your email for verification code.'
    })


@csrf_exempt
def mailVerification(request):
    try:
        body = json.loads(request.body)
        cod = body.get('codVerificare')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

    codeVer = request.session['codeVerificare']
    print(cod)
    print(codeVer)
    if cod == str(codeVer):
        name = request.session['name']
        age = request.session['age']
        username = request.session['username']
        mail = request.session['mail']
        phoneNumber = request.session['phoneNumber']
        password = request.session['password']
        nextUserId = int(request.session['nextUserId'])
        generareIban = request.session['generareIban']
        newUser = User(name, age, username, password, mail, phoneNumber, nextUserId)
        contBancar = ContBancar(nextUserId, 'RON', 1000, generareIban)
        mongo = MongoDBConnect()
        tabel = DataBaseTabel(mongo.get_tabel("DB_User", "Users"))
        tabel.add(newUser)
        tabel = DataBaseTabel(mongo.get_tabel("DB_User", "conturi"))
        tabel.add(contBancar)

        request.session['userID'] = str(newUser.userID)
        request.session['cont'] = contBancar.toDic()

        return JsonResponse({'message': 'User successfully created. You can now log in.'})
    return JsonResponse({'error': 'Invalid verification code'}, status=400)
