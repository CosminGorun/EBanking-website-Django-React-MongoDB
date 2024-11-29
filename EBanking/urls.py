from django.urls import path

from EBanking.views import viewLoginClient,viewCreateAccount,viewTranzactii,viewMainPage

urlpatterns=[
    #path('',viewLoginClient.goToLoginClient,name='goToLoginClient'),
    # path('addPers',view.addPers,name='addPers'),

    path('mainPage', viewMainPage.mainPage, name='mainPage'),

     path('transferConturi',viewTranzactii.transferConturi,name='transferConturi'),
     path('finalizareTransfer',viewTranzactii.finalizareTransfer,name='finalizareTransfer'),

     path('cancelTransfer',viewTranzactii.cancelTransfer,name='cancelTransfer'),
     path('loginClient',viewLoginClient.loginClient,name='loginClient'),
     path('goToLoginClient',viewLoginClient.goToLoginClient,name='goToLoginClient'),

     path('goToCreateAccount',viewCreateAccount.goToCreateAccount,name='goToCreateAccount'),
     path('createAccount',viewCreateAccount.createAccount,name='createAccount'),
     path('mailVerification',viewCreateAccount.mailVerification,name='mailVerification'),


    ]
