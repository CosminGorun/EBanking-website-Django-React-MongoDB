from django.urls import path

from . import views

urlpatterns=[
    path('',views.loginClient,name='loginClient'),
    path('addPers',views.addPers,name='addPers'),
     path('loginClient',views.loginClient,name='loginClient'),
     path('goToCreateAccount',views.goToCreateAccount,name='goToCreateAccount'),
     path('createAccount',views.createAccount,name='createAccount'),
    ]
