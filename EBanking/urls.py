from django.urls import path

from . import views

urlpatterns=[
    path('',views.loginClient,name='loginClient'),
    path('addPers',views.addPers,name='addPers'),
     path('loginClient',views.loginClient,name='loginClient'),
]