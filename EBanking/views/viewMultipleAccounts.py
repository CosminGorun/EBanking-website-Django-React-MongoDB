from locale import currency

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from DataBase.Connection.MongoDBConnect import MongoDBConnect
from DataBase.DataBaseUC.TabelOperation import DataBaseTabel
from DataBase.DB_Data.ContBancar import ContBancar
from random import randint, random
import json

tabelaCont = "conturi"
dbCont = "DB_User"


def generareIban(moneda):
    iban = moneda
    iban += str(randint(100, 999))
    iban += "SIG"
    iban += str(randint(10 ** 9, 10 ** 10 - 1))
    return iban

@csrf_exempt
def addAccount(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
    userID = int(request.session['userID'])
    actCurrency=body.get('currency')
    actCurrency=actCurrency.upper()
    print("UserID:"+str(userID))
    print("Currency:"+str(actCurrency[:2]))
    IBAN = generareIban(actCurrency[:2])
    contBancar = ContBancar(userID, actCurrency, 0, IBAN)

    mongo = MongoDBConnect()
    tabelCont = DataBaseTabel(mongo.get_tabel(dbCont, tabelaCont))
    tabelCont.add(contBancar)
    print(contBancar.toDic())


    return JsonResponse({'message': 'Account successfully created.'})
