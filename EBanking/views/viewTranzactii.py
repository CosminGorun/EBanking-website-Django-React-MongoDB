from DataBase.Connection.MongoDBConnect import MongoDBConnect
from DataBase.DataBaseUC.TabelOperation import DataBaseTabel
from EBanking.views.viewMainPage import mainPage

tabelaCont="ionut2"
dbCont="test1"

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