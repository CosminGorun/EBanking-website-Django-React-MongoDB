import json
from random import randint
from types import NoneType

from DataBase.DB_Data.User import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from DataBase.Connection.MongoDBConnect import MongoDBConnect
from DataBase.DataBaseUC.TabelOperation import DataBaseTabel
from DataBase.EmailSender.Sender import EmailSender


def generateCode():
    return randint(100000, 999999)
@csrf_exempt
def forgotPassword(request):
    try:
        body = json.loads(request.body)
        username = body.get('username')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
    mongo = MongoDBConnect()
    tabel = DataBaseTabel(mongo.get_tabel("DB_User", "Users"))
    user= tabel.findOneBy({'username':username})
    if user is None:
        return JsonResponse({'error': 'Username gresit'}, status=400)
    mail=user.get("mail")
    codeVerificare = generateCode()
    email = EmailSender()
    string = "Codul este "
    string += str(codeVerificare)
    email.sendMail(mail, "cod verificare", string)
    request.session['codeVerificare'] = codeVerificare
    request.session['username'] = username
    return JsonResponse({
        'message': 'Account created successfully. Please check your email for verification code.'
    })

@csrf_exempt
def mailVerificationPass(request):
    try:
        body = json.loads(request.body)
        cod = body.get('codVerificare')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
    if cod == str(request.session['codeVerificare']):
        return JsonResponse({'message': 'User successfully created. You can now log in.'})
    return JsonResponse({'error': 'Invalid verification code'}, status=400)

@csrf_exempt
def changePassword(request):
    try:
        body = json.loads(request.body)
        username = request.session['username']
        password = body.get('newPassword')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
    mongo = MongoDBConnect()
    tabel = DataBaseTabel(mongo.get_tabel("DB_User", "Users"))
    user=tabel.findOneBy({'username':username})
    oldPassword=user.get("password")
    if oldPassword==password :
        return JsonResponse({'message': 'You cannot use the old password.'}, status=400)
    user['password']=password
    tabel.updateOne({'username':username},user)
    return JsonResponse({'message': 'Password changed successfully.'})