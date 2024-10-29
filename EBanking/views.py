from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def mainPage(request):
    return render(request, 'mainPage.html')