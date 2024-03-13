from django.shortcuts import render, HttpResponse
from django.urls import path, include
from .models import Getdata

# Create your views here.
def index(request):
    getform = Getdata()
    context = {
        'getform' : getform
    }
    is_get_request = request.method == 'GET'
    is_v_in_get = 'v' in request.GET   
    return render(request, 'home.html', {
        'is_get_request': is_get_request,
        'is_v_in_get': is_v_in_get,
        'is_v' : request.GET.get('v', None)
    })

def about(request):
    return render(request, 'about.html')

def video_download(request):
    getform = Getdata()
    context = {
        'getform' : getform
    }   
    return render(request, 'video-download.html', context)

def audio_download(request):
    getform = Getdata()
    context = {
        'getform' : getform
    }   
    return render(request, 'audio-download.html', context)

def shorts_download(request):
    getform = Getdata()
    context = {
        'getform' : getform
    }   
    return render(request, 'shorts-download.html', context)

# def about(request):
#     return HttpResponse('aboutpage')

def contact(request):
    return HttpResponse('contactpage')
