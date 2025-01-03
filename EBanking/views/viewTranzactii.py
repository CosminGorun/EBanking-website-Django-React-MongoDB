from DataBase.Connection.MongoDBConnect import MongoDBConnect
from DataBase.DB_Data.Transfer import Transfer
from DataBase.DataBaseUC.TabelOperation import DataBaseTabel
from EBanking.views.viewMainPage import mainPage
from EBanking.views.viewMainPage import dbTr
from EBanking.views.viewMainPage import tabelaTr,tabelaUser,dbUser
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import requests
tabelaCont="conturi"
dbCont="DB_User"
country_currency = {
    "RO": "RON",
    "HU": "HUF",
    "EU": "EUR",
    "US": "USD"
}
def convValutar(from_val,to_val):
    url = "https://api.frankfurter.app/latest?from={}&to={}".format(from_val,to_val)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['rates'][to_val]

    return 1
def gasesteValutaIban(iban):
    for key, value in country_currency.items():
        if key == iban[:2]:
            return value
    return "RON"
def gasesteCurs(ibanSursa,ibanDestinatie):
    cursSursa=gasesteValutaIban(ibanSursa)
    cursDestinatie=gasesteValutaIban(ibanDestinatie)
    return convValutar(cursSursa,cursDestinatie)

@csrf_exempt
def transferConturi(request):
    userPrincipal = request.session.get('userID')
    contPrincipal = cont = request.session.get('cont')
    if request.method != "POST":
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    try:
        print("Raw request body:", request.body)
        body = json.loads(request.body)
        ibanDestinatie = body.get('ibanDestinatie')
        suma = float(body.get('suma'))
        ibanSursa = str(body.get('ibanSursa'))
        userID = int(body.get('userID'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request payload'}, status=401)
    mongo = MongoDBConnect()
    tabel = DataBaseTabel(mongo.get_tabel("DB_User", "Users"))
    tabelCont=DataBaseTabel(mongo.get_tabel(dbCont,tabelaCont))
    tabelTr=DataBaseTabel(mongo.get_tabel(dbTr,tabelaTr))
    valutaSursa=gasesteValutaIban(ibanSursa)
    sumaConv=suma
    print(ibanDestinatie)
    print(ibanSursa)
    # print(f"Curs valutar={cursVal}")
    err=""
    user=tabel.findOneBy({"userID":int(userID)})
    cont=tabelCont.findOneBy({"iban":ibanSursa})
    if cont is None:
        print("Contul nu exista!")
        return JsonResponse({'error': 'Contul nu exista'}, status=400)
    soldUser=float(cont["sold"])
    contDest=tabelCont.findOneBy({"iban":ibanDestinatie})
    transferuri = tabelTr.getAll(Transfer)
    transfTotal=0
    for transfer in transferuri:
        if transfer.IBANtrimite==ibanSursa and transfer.finalizat==0:
            transfTotal+=float(transfer.sumaTransfer)
    if contDest==cont:
        return JsonResponse({'error': 'Contul destinatie nu poate sa fie contul sursa!'}, status=400)
    if contDest is None:
        return JsonResponse({'error': 'Contul destinatie nu exista!'}, status=400)
    if soldUser-suma<0:
        return JsonResponse({'error': 'Contul are soldul prea mic pentru a efectua tranzactia!'}, status=400)
    if soldUser-suma<0:
        print(soldUser)
        print(suma)
        print(transfTotal)
        return JsonResponse({'error': 'Contul are soldul suficient dar are tranzactii pending care il opresc sa faca tranzactia!'}, status=400)
    #nu am adaugat verificari pt testare

    print(f"Suma={suma}")
    contDestUpdated=contDest.copy()
    contUpdated=cont.copy()
    # contDestUpdated["sold"]=str(float(contDest["sold"])+suma)#soldul trb facut int UPS :(
    contUpdated['sold']=str(float(cont['sold'])-suma)
    # tabelCont.updateOne(cont,cont2)
    # tabelCont.updateOne(contDest, contDest2)
    idTransfer=0
    for transfer in transferuri:
        if transfer.IDTransfer>idTransfer:
            idTransfer=transfer.IDTransfer
    idTransfer+=1
    print(f"sumaConv={sumaConv}")
    newTransfer=Transfer(idTransfer, ibanSursa, ibanDestinatie, sumaConv, valutaSursa, str(date.today()), 0)

    tabelTr.add(newTransfer)
    #urmeaza sa adaug si in tabela de transfer
    tabelCont.updateOne(cont, contUpdated)
    tabelCont.updateOne(contDest, contDestUpdated)

    if contUpdated:
        contUpdated['_id'] = str(contUpdated['_id'])
    request.session['cont'] = contUpdated
    #request.session.modified = True
    #request.session.save()

    return JsonResponse({'message': 'Transfer initiated successfully', 'transferID': idTransfer})

@csrf_exempt
def finalizareTransfer(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    try:
        body = json.loads(request.body)
        action = body.get('action')
        IDTransfer = int(body.get('IDTransfer'))
    except (json.JSONDecodeError, TypeError, ValueError):
        return JsonResponse({'error': 'Invalid request payload2'}, status=400)

    mongo = MongoDBConnect()
    tabel = DataBaseTabel(mongo.get_tabel("DB_User", "Users"))
    tabelCont=DataBaseTabel(mongo.get_tabel(dbCont,tabelaCont))
    tabelTr=DataBaseTabel(mongo.get_tabel(dbTr,tabelaTr))
    if action=="accept":
        transfer = tabelTr.findOneBy({"IDTransfer": int(IDTransfer)})
        cont=tabelCont.findOneBy({"iban":transfer["IBANprimeste"]})
        contTrimite=tabelCont.findOneBy({"iban":transfer["IBANtrimite"]})
        user=tabel.findOneBy({"userID":int(cont["userID"])})
        suma=float(transfer["sumaTransfer"])
        contTrimite2=contTrimite.copy()
        cont2=cont.copy()
        transfer2=transfer.copy()
        # contTrimite2["sold"]=str(float(contTrimite["sold"])-suma)
        cursVal = gasesteCurs(transfer["IBANtrimite"], transfer["IBANprimeste"])
        cont2['sold']=str(float(cont['sold'])+cursVal*suma)
        transfer2["finalizat"]=1
        tabelCont.updateOne(cont,cont2)
        tabelCont.updateOne(contTrimite, contTrimite2)
        tabelTr.updateOne(transfer,transfer2)
        if cont2:
            cont2['_id'] = str(cont2['_id'])
        request.session['cont'] = cont2
        return JsonResponse({'message': 'Transfer accepted successfully'})
    else:
        transfer = tabelTr.findOneBy({"IDTransfer": int(IDTransfer)})
        cont = tabelCont.findOneBy({"iban": transfer["IBANtrimite"]})
        suma = float(transfer["sumaTransfer"])
        cont3 = cont.copy()
        cont3['sold'] = str(float(cont['sold']) + suma)
        tabelCont.updateOne(cont, cont3)
        user = tabel.findOneBy({"userID": int(cont["userID"])})
        transfer2 = transfer.copy()
        transfer2["finalizat"] = 2
        tabelTr.updateOne(transfer, transfer2)

        cont = tabelCont.findOneBy({"iban": transfer["IBANprimeste"]})
        if cont:
            cont['_id'] = str(cont['_id'])
        request.session['cont'] = cont
        return JsonResponse({'message': 'Transfer rejected successfully'})

@csrf_exempt
def cancelTransfer(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    try:
        body = json.loads(request.body)
        IDTransfer = int(body.get('IDTransfer'))
    except (json.JSONDecodeError, TypeError, ValueError):
        return JsonResponse({'error': 'Invalid request payload3'}, status=400)

    mongo = MongoDBConnect()
    tabel = DataBaseTabel(mongo.get_tabel("DB_User", "Users"))
    tabelCont = DataBaseTabel(mongo.get_tabel(dbCont, tabelaCont))
    tabelTr = DataBaseTabel(mongo.get_tabel(dbTr, tabelaTr))

    transfer = tabelTr.findOneBy({"IDTransfer": int(IDTransfer)})

    if transfer is None:
        return JsonResponse({'error': 'Transfer not found'}, status=400)

    cont = tabelCont.findOneBy({"iban": transfer["IBANtrimite"]})
    if cont is None:
        return JsonResponse({'error': 'Source or destination account not found'}, status=400)

    user = tabel.findOneBy({"userID": int(cont["userID"])})
    suma=float(transfer["sumaTransfer"])
    #print("\n\ncont:")
    #print(cont['sold'])
    contUpdated=cont.copy()
    contUpdated['sold']=str(float(contUpdated['sold'])+suma)
    #print("\n\nsold nou")
    #print(cont['sold'])
    transfer2 = transfer.copy()
    transfer2["finalizat"] = 2
    tabelCont.updateOne(cont, contUpdated)
    tabelTr.updateOne(transfer, transfer2)

    if cont:
            contUpdated['_id'] = str(contUpdated['_id'])
    request.session['cont'] = contUpdated
    request.session.modified = True
    request.session.save()

    return JsonResponse({'message': 'Transfer cancelled successfully'})

tabelaTr="ionut3"
dbTr="test1"
@csrf_exempt
def gaseste_cont(request):
    ibanCont = request.GET.get('contIBAN')
    mongo = MongoDBConnect()
    tabelCont = DataBaseTabel(mongo.get_tabel(dbCont, tabelaCont))
    tabelTr = DataBaseTabel(mongo.get_tabel(dbTr, tabelaTr))
    listTr = tabelTr.getAll(Transfer)
    cont = tabelCont.findOneBy({"iban": ibanCont})
    tabelUser = DataBaseTabel(mongo.get_tabel(dbUser, tabelaUser))
    if cont:
        cont['_id'] = str(cont['_id'])
    tranzactiiUserOUT=[]
    tranzactiiUserIN = []
    conturiIBAN=[]
    # request.session['cont'] = cont
    # request.session.modified = True
    # request.session.save()
    user = tabelUser.findOneBy({"userID": int(cont['userID'])})
    userName = user['name']
    for tranzactie in listTr:
        if tranzactie.IBANprimeste == cont["iban"] and tranzactie.finalizat == 0:
            tranzactiiUserOUT.append(tranzactie)
        if tranzactie.IBANtrimite == cont["iban"] and tranzactie.finalizat == 0:
            tranzactiiUserIN.append(tranzactie)
        # print([transaction.toDic() for transaction in tranzactiiUserIN])
    response_data = {
        'tranzactiiUserOUT': [transaction.toDic() for transaction in tranzactiiUserOUT],
        'tranzactiiUserIN': [transaction.toDic() for transaction in tranzactiiUserIN],
        'USERID': cont['userID'],
        'NAME': userName,
        'CONT': cont
    }
    return JsonResponse(response_data)