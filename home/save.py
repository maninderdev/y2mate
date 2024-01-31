from django.shortcuts import render, HttpResponse
from django.urls import path, include
from django.http import JsonResponse
from home.youtubedl.youtube_dl.YoutubeDL import YoutubeDL

# Create your views here.
def saveData(request):
    if request.method == 'GET':
        if request.method == 'GET' and 'id' in request.GET:
            product_id = request.GET['id']


            def my_hook(d):
                if d['status'] == 'finished':
                    print('Done downloading, now converting ...')


            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': 'test.%(ext)s',
                'progress_hooks': [my_hook],
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download(['https://www.youtube.com/watch?v='+product_id])
            return HttpResponse(product_id)
        else:
            product_id = 0
            return HttpResponse('A file should be downloaded')
    else:
        return HttpResponse('🤣')