from django.shortcuts import render, HttpResponse
from django.urls import path, include
from .models import Getdata

# Create your views here.
def index(request):
    getform = Getdata()
    context = {
        'getform' : getform
    }   
    return render(request, 'home.html', context)

def about(request):
    return HttpResponse('aboutpage')

def contact(request):
    return HttpResponse('contactpage')
