from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from DataBase.Connection.MongoDBConnect import MongoDBConnect
from DataBase.DataBaseUC.TabelOperation import DataBaseTabel
from DataBase.DB_Data.ContBancar import ContBancar
import json

tabelaCont = "conturi"
dbCont = "DB_User"


@csrf_exempt
def view_multiple_accounts(request):
    if not request.session.get('userID'):
        return JsonResponse({'error': 'User not logged in!'}, status=401)

    user_id = int(request.session.get('userID'))  # Get logged-in user's ID from session

    mongo = MongoDBConnect()
    tabelCont = DataBaseTabel(mongo.get_tabel(dbCont, tabelaCont))

    # Retrieve all accounts belonging to the user
    user_accounts = tabelCont.findAllBy({"userID": user_id})

    if not user_accounts:
        return JsonResponse({'message': "No accounts found for the user."}, status=404)

    # Prepare the response with account details
    accounts_data = [ContBancar.fromDict(account).toDic() for account in user_accounts]

    return JsonResponse({
        'message': 'Accounts retrieved successfully!',
        'accounts': accounts_data
    })
