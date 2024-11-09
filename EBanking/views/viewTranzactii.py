from DataBase.Connection.MongoDBConnect import MongoDBConnect
from DataBase.DB_Data.Transfer import Transfer
from DataBase.DataBaseUC.TabelOperation import DataBaseTabel
from EBanking.views.viewMainPage import mainPage
from EBanking.views.viewMainPage import dbTr
from EBanking.views.viewMainPage import tabelaTr
from datetime import date
tabelaCont="ionut2"
dbCont="test1"



def transferConturi(request):
    mongo = MongoDBConnect()
    tabel = DataBaseTabel(mongo.get_tabel("DB_User", "Users"))
    tabelCont=DataBaseTabel(mongo.get_tabel(dbCont,tabelaCont))
    tabelTr=DataBaseTabel(mongo.get_tabel(dbTr,tabelaTr))
    err=""
    ibanSursa=request.POST.get('ibanSursa')
    ibanDestinatie=request.POST.get('ibanDestinatie')
    suma=int(request.POST.get('suma'))
    val=request.POST.get('userID')
    user=tabel.findOneBy({"userID":int(val)})
    cont=tabelCont.findOneBy({"iban":ibanSursa})
    soldUser=int(cont["sold"])
    contDest=tabelCont.findOneBy({"iban":ibanDestinatie})
    transferuri = tabelTr.getAll(Transfer)
    transfTotal=0
    for transfer in transferuri:
        if transfer.IBANtrimite==ibanSursa and transfer.finalizat==0:
            transfTotal+=int(transfer.sumaTransfer)
    if contDest==cont:
        err="Contul destinatie nu poate sa fie contul sursa!"
        return mainPage(request,user,cont,err)#cont gresit (nu am mai adugat html, urmeaza)
    if contDest is None:
        err="Contul destinatie nu exista!"
        return mainPage(request,user,cont,err)#cont gresit (nu am mai adugat html, urmeaza)
    if soldUser-suma<0:
        err="Contul are soldul prea mic pentru a efectua tranzactia!"
        return mainPage(request, user, cont, err)  # cont gresit (nu am mai adugat html, urmeaza)
    if soldUser-suma-transfTotal<0:
        err="Contul are soldul suficient dar are tranzactii pending care il opresc sa faca tranzactia!"
        return mainPage(request, user, cont, err)  # cont gresit (nu am mai adugat html, urmeaza)
    #nu am adaugat verificari pt testare
    contDest2=contDest.copy()
    cont2=cont.copy()
    contDest2["sold"]=str(int(contDest["sold"])+suma)#soldul trb facut int UPS :(
    cont2['sold']=str(int(cont['sold'])-suma)
    # tabelCont.updateOne(cont,cont2)
    # tabelCont.updateOne(contDest, contDest2)
    idTransfer=0
    for transfer in transferuri:
        if transfer.IDTransfer>idTransfer:
            idTransfer=transfer.IDTransfer
    idTransfer+=1
    tabelTr.add(Transfer(idTransfer,ibanSursa,ibanDestinatie,int(suma),'RON',str(date.today()),0))
    #urmeaza sa adaug si in tabela de transfer
    return mainPage(request,user,cont)

def finalizareTransfer(request):
    mongo = MongoDBConnect()
    tabel = DataBaseTabel(mongo.get_tabel("DB_User", "Users"))
    tabelCont=DataBaseTabel(mongo.get_tabel(dbCont,tabelaCont))
    tabelTr=DataBaseTabel(mongo.get_tabel(dbTr,tabelaTr))
    action = request.POST.get('action')
    IDTransfer = request.POST.get('IDTransfer')
    if action=="accept":
        transfer = tabelTr.findOneBy({"IDTransfer": int(IDTransfer)})
        cont=tabelCont.findOneBy({"iban":transfer["IBANprimeste"]})
        contTrimite=tabelCont.findOneBy({"iban":transfer["IBANtrimite"]})
        user=tabel.findOneBy({"userID":int(cont["userID"])})
        suma=transfer["sumaTransfer"]
        contTrimite2=contTrimite.copy()
        cont2=cont.copy()
        transfer2=transfer.copy()
        contTrimite2["sold"]=str(int(contTrimite["sold"])-suma)#soldul trb facut int UPS :(
        cont2['sold']=str(int(cont['sold'])+suma)
        transfer2["finalizat"]=1
        tabelCont.updateOne(cont,cont2)
        tabelCont.updateOne(contTrimite, contTrimite2)
        tabelTr.updateOne(transfer,transfer2)
        return mainPage(request,user,cont2)
    else:
        transfer = tabelTr.findOneBy({"IDTransfer": int(IDTransfer)})
        cont = tabelCont.findOneBy({"iban": transfer["IBANprimeste"]})
        user = tabel.findOneBy({"userID": int(cont["userID"])})
        transfer2 = transfer.copy()
        transfer2["finalizat"] = 2
        tabelTr.updateOne(transfer, transfer2)
        return mainPage(request, user, cont)

def cancelTransfer(request):
    mongo = MongoDBConnect()
    tabel = DataBaseTabel(mongo.get_tabel("DB_User", "Users"))
    tabelCont = DataBaseTabel(mongo.get_tabel(dbCont, tabelaCont))
    tabelTr = DataBaseTabel(mongo.get_tabel(dbTr, tabelaTr))
    IDTransfer = request.POST.get('IDTransfer')
    transfer = tabelTr.findOneBy({"IDTransfer": int(IDTransfer)})
    cont = tabelCont.findOneBy({"iban": transfer["IBANtrimite"]})
    user = tabel.findOneBy({"userID": int(cont["userID"])})
    transfer2 = transfer.copy()
    transfer2["finalizat"] = 2
    tabelTr.updateOne(transfer, transfer2)
    return mainPage(request,user,cont)