from django.urls import path

from EBanking.views import viewLoginClient, viewCreateAccount, viewTranzactii, viewMainPage, viewMultipleAccounts, \
 viewRecoverPassword

urlpatterns=[
    #path('',viewLoginClient.goToLoginClient,name='goToLoginClient'),
    # path('addPers',view.addPers,name='addPers'),

    path('mainPage', viewMainPage.mainPage, name='mainPage'),

     path('transferConturi',viewTranzactii.transferConturi,name='transferConturi'),
     path('finalizareTransfer',viewTranzactii.finalizareTransfer,name='finalizareTransfer'),

     path('cancelTransfer',viewTranzactii.cancelTransfer,name='cancelTransfer'),

     path('gaseste_cont',viewTranzactii.gaseste_cont,name='gaseste_cont'),

     path('getTransferuri',viewTranzactii.getTransferuri,name='getTransferuri'),
     path('loginClient',viewLoginClient.loginClient,name='loginClient'),
     path('goToLoginClient',viewLoginClient.goToLoginClient,name='goToLoginClient'),

     path('goToCreateAccount',viewCreateAccount.goToCreateAccount,name='goToCreateAccount'),
     path('createAccount',viewCreateAccount.createAccount,name='createAccount'),
     path('mailVerification',viewCreateAccount.mailVerification,name='mailVerification'),


     path('addAccount', viewMultipleAccounts.addAccount, name='addAccount'),
     path('forgotPassword', viewRecoverPassword.forgotPassword, name='forgotPassword'),
     path('mailVerificationPass', viewRecoverPassword.mailVerificationPass, name='mailVerificationPass'),
     path('changePassword', viewRecoverPassword.changePassword, name='changePassword'),


    ]
