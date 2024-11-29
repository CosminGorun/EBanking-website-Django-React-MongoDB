from django.http import JsonResponse
from django.shortcuts import render
from DataBase.Connection.MongoDBConnect import MongoDBConnect
from DataBase.DB_Data.Person import Person
from DataBase.DB_Data.Transfer import Transfer
from DataBase.DataBaseUC.TabelOperation import DataBaseTabel
from django.views.decorators.csrf import csrf_exempt

tabelaTr="ionut3"
dbTr="test1"

@csrf_exempt
def mainPage(request,context=None):
    mongo=MongoDBConnect()
    tabel=DataBaseTabel(mongo.get_tabel("test1","ai"))
    tabelTr = DataBaseTabel(mongo.get_tabel(dbTr, tabelaTr))
    # listPers=tabel.getAll(Person)
    listTr=tabelTr.getAll(Transfer)
    tranzactiiUserOUT=[]
    tranzactiiUserIN = []

    userID = request.session.get('userID')
    cont = request.session.get('cont')

    #print(cont.get("iban"))

    if userID is None or cont is None:
        return JsonResponse({'error': 'User or account data missing from session.'}, status=400)

    for tranzactie in listTr:
        if tranzactie.IBANprimeste==cont["iban"] and tranzactie.finalizat==0:
            tranzactiiUserOUT.append(tranzactie)
        if tranzactie.IBANtrimite==cont["iban"] and tranzactie.finalizat==0:
            tranzactiiUserIN.append(tranzactie)

    #print("tranzactii in\n")
    #print(tranzactiiUserIN)
    #print("tranzactiio out\n\n")
    #print(tranzactiiUserOUT)
    print("\nsoldul nou este")
    print(cont['sold'])

    response_data = {
        'tranzactiiUserOUT': [transaction.toDic() for transaction in tranzactiiUserOUT],  
        'tranzactiiUserIN': [transaction.toDic() for transaction in tranzactiiUserIN],    
        'USERID': userID,
        'CONT': cont
    }

    return JsonResponse(response_data)
