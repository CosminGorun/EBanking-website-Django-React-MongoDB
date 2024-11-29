from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.shortcuts import render
from DataBase.Connection.MongoDBConnect import MongoDBConnect
from DataBase.DataBaseUC.TabelOperation import DataBaseTabel
from EBanking.views.viewMainPage import mainPage
from HtmlContent.ContextClass import LoginClientContext,CreateAccountContext
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
import json

tabelaCont="ionut2"
dbCont="test1"
def goToLoginClient(request):
    return render(request, 'Login.html')

@csrf_exempt
def loginClient(request):
    try:
        body = json.loads(request.body)
        username = body.get('username')
        password = body.get('password')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400)

    mongo = MongoDBConnect()
    tabel = DataBaseTabel(mongo.get_tabel("DB_User", "Users"))
    tabelCont = DataBaseTabel(mongo.get_tabel(dbCont, tabelaCont))
    #username = request.POST.get('username')
    #password = request.POST.get('password')
    context=LoginClientContext()
    user=tabel.findOneBy({"username":username})

    if user is None:
        context.ErUserName="User-ul nu a fost gasit!"
        return JsonResponse({'error': context.ErUserName}, status=400)
    else:
        if user['password'] != password:
            context.ErPassword="Parola gresita!"
            return JsonResponse({'error': context.ErPassword}, status=400)
    cont = tabelCont.findOneBy({"userID": user['userID']}) # daca s-a validat user-ul inseamna ca are si userId :D asa ca nu verific nimic

    user['userID'] = str(user['userID'])
    if cont:
        cont['_id'] = str(cont['_id'])  

    request.session['userID'] = str(user['userID'])
    request.session['cont'] = cont  

    print("Stored in session:", request.session['userID'], request.session['cont'])

    response_data = {
        'username': user['username'],
        'userID': user['userID'],
        'cont': cont,  
        'message': 'Login successful'
    }
    return JsonResponse(response_data)