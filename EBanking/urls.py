from django.urls import path

from . import views

urlpatterns=[
    path('',views.goToLoginClient,name='goToLoginClient'),
    path('addPers',views.addPers,name='addPers'),
     path('loginClient',views.loginClient,name='loginClient'),
     path('goToLoginClient',views.goToLoginClient,name='goToLoginClient'),

     path('goToCreateAccount',views.goToCreateAccount,name='goToCreateAccount'),
     path('createAccount',views.createAccount,name='createAccount'),
    ]
