from django.contrib import admin
from django.urls import path, include
from home import views
from home.get import ( fetchdata )
from home.get import ( downloadContext )
from home.save import ( saveData )

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('post/data', fetchdata, name='fetchdata'),
    path('post/download', downloadContext, name='downloadContext'),
    path('post/save', saveData, name='saveData'),
]
