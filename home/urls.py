from django.contrib import admin
from django.urls import path, include
from home import views
from home.get import ( fetchdata )
from home.get import ( downloadContext )
from home.get import ( progress )
from home.save import ( saveData )

urlpatterns = [
    path('', views.index, name='home'),
    path('shorts-download', views.shorts_download, name='shorts_download'),
    path('audio-download', views.audio_download, name='audio_download'),
    path('video-download', views.video_download, name='video_download'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('post/data', fetchdata, name='fetchdata'),
    path('post/download', downloadContext, name='downloadContext'),
    path('post/progress', progress, name='progress'),
    path('post/save', saveData, name='saveData'),
]
