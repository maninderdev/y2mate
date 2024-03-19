from django.shortcuts import render, HttpResponse
from django.urls import path, include

# Create your views here.
def index(request):
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
    return render(request, 'video-download.html')

def audio_download(request):
    return render(request, 'audio-download.html')

def shorts_download(request):
    return render(request, 'shorts-download.html')

# def about(request):
#     return HttpResponse('aboutpage')

def contact(request):
    return HttpResponse('contactpage')
