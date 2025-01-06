from django.http import JsonResponse
from django.shortcuts import render
from DataBase.Connection.MongoDBConnect import MongoDBConnect
from DataBase.DB_Data.ContBancar import ContBancar
from DataBase.DB_Data.Person import Person
from DataBase.DB_Data.Transfer import Transfer
from DataBase.DataBaseUC.TabelOperation import DataBaseTabel
from django.views.decorators.csrf import csrf_exempt

tabelaTr="ionut3"
dbTr="test1"

tabelaCont="conturi"
dbCont="DB_User"

tabelaUser = "Users"
dbUser = "DB_User"
@csrf_exempt

def mainPage(request,context=None):
    mongo=MongoDBConnect()
    # tabel=DataBaseTabel(mongo.get_tabel("test1","ai"))
    tabelTr = DataBaseTabel(mongo.get_tabel(dbTr, tabelaTr))
    tabelCont = DataBaseTabel(mongo.get_tabel("DB_User", "conturi"))
    tabelUser = DataBaseTabel(mongo.get_tabel(dbUser, tabelaUser))
    # listPers=tabel.getAll(Person)
    listTr=tabelTr.getAll(Transfer)
    tranzactiiUserOUT=[]
    tranzactiiUserIN = []
    conturiIBAN=[]
    transferuriAcceptate=[]
    transferuriRejectate=[]
    print("Salut")
    userID = request.session.get('userID')
    cont = request.session.get('cont')
    elemente=tabelCont.getAll(ContBancar)
    for element in elemente:
        print("userID"+str(element.userID))
        print("userIDPRI=",userID)
        if element.userID==int(userID):
            conturiIBAN.append(element.iban)
    print("Conturi=")
    for contIBAN in conturiIBAN:
        print("Cont="+contIBAN)


    user = tabelUser.findOneBy({"userID": int(userID)})
    userName=user['name']
    #print(cont.get("iban"))

    if userID is None or cont is None:
        return JsonResponse({'error': 'User or account data missing from session.'}, status=400)

    for tranzactie in listTr:
        if tranzactie.IBANprimeste == cont["iban"]:
            if tranzactie.finalizat == 0:
                tranzactiiUserOUT.append(tranzactie)
            else:
                transferuriAcceptate.append(tranzactie)
        if tranzactie.IBANtrimite == cont["iban"] :
            if tranzactie.finalizat == 0:
                tranzactiiUserIN.append(tranzactie)
            else:
                transferuriRejectate.append(tranzactie)

    #print("tranzactii in\n")
    #print(tranzactiiUserIN)
    #print("tranzactiio out\n\n")
    #print(tranzactiiUserOUT)
    print("\nsoldul nou este")
    print(cont['sold'])

    response_data = {
        'tranzactiiUserOUT': [transaction.toDic() for transaction in tranzactiiUserOUT],  
        'tranzactiiUserIN': [transaction.toDic() for transaction in tranzactiiUserIN],
        'transferuriAcceptate': [transaction.toDic() for transaction in transferuriAcceptate],
        'transferuriRejectate': [transaction.toDic() for transaction in transferuriRejectate],
        'conturiIBAN':conturiIBAN,
        'USERID': userID,
        'NAME':userName,
        'CONT': cont,
        'MONEDA': cont['moneda']
    }

    return JsonResponse(response_data)
