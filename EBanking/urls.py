from django.urls import path

from . import views

urlpatterns=[
    path('',views.mainPage,name='mainPage'),
    path('addPers',views.addPers,name='addPers'),
     path('loginClient',views.loginClient,name='loginClient'),
]