from django.shortcuts import render
from DataBase.Connection.MongoDBConnect import MongoDBConnect
from DataBase.DataBaseUC.TabelOperation import DataBaseTabel
from EBanking.views.viewMainPage import mainPage
from HtmlContent.ContextClass import LoginClientContext,CreateAccountContext

tabelaCont="ionut2"
dbCont="test1"
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