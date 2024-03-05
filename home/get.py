from django.shortcuts import render, HttpResponse
from django.urls import path, include
from django.http import JsonResponse
import urllib.parse, urllib.request
import os
# from youtube_dl import YoutubeDL
from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip, AudioFileClip
currentProgress = "Donetest"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Create your views here.
def fetchdata(request):
    if request.method == 'POST':
        url = request.POST['get']
        ydl = YoutubeDL()
        ydl.cache.remove()
        r = ydl.extract_info(url, download=False)
        # if any link will do 
        data = [{'formats': r['formats'], 'thumbnail' : r['thumbnail'], 'title' : r['title']}]
        # datas = data.objects.values('structure').annotate(
            # total=Count('structure')
        # ).order_by('-total')
        # dataStructure = json.dumps(list(data), cls=DjangoJSONEncoder)
        print(data)
        # dataStructure = serializers.serialize("json",data, fields=('structure',))
        # if you want links with video and audio
        # urls = [f['url'] for f in r['formats'] if f['acodec'] != 'none' and f['vcodec'] != 'none']

        return JsonResponse(data, safe=False)
    else:
        return HttpResponse('Error error')
    

def downloadContext(request):
    if request.method == 'GET' and 'format' in request.GET:
        class MyLogger(object):
            def debug(self, msg):
                pass

            def warning(self, msg):
                pass

            def error(self, msg):
                print(msg)



        global currentProgress
        currentProgress = 0
        def my_hook(d):
            global currentProgress
            if d['status'] == 'downloading':
                currentProgress = d['_percent_str']
                print(d['_percent_str'])
                return d['_percent_str']
            elif d['status'] == 'finished':
                global fetchFile
                fetchFile = d['filename']


        dlformat = request.GET['format']
        dlext = request.GET['ext']
        dlType = 'video'
        if(request.GET['type'] == 'audio'):
            dlType = 'audio'


        ydl_format = dlformat
        
        if 'merge' in request.GET:
            ydl_format = dlformat+'+'+request.GET['merge']

        ydl_opts = {
            'format': ydl_format,
            'logger': MyLogger(),
            'outtmpl': '/context/'+dlType+'/'+request.GET['format']+'/%(title)s-%(id)s.%(ext)s',
            'progress_hooks': [my_hook]
        }


        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://www.youtube.com/watch?v='+request.GET['dlId']])

        
        if(fetchFile):
            fetchFileMerge = fetchFile
            print(fetchFileMerge)
            if 'merge' in request.GET:
                fetchFileMerge = fetchFile.replace('.f140.m4a', '')
                fetchFileMerge = fetchFileMerge+".mp4"
            
            print(fetchFileMerge)
            with open(os.path.join(BASE_DIR+'/'+fetchFileMerge), 'rb') as f:
                filename = os.path.basename(f.name).split('/')[-1]
                data = f.read()
            response = HttpResponse(data, content_type='application/'+dlType+'.'+dlext+'')
            filename_bytes = filename.encode('utf8')
            decoded_filename = urllib.parse.unquote(filename_bytes.decode('utf-8'))
            quoted_filename = urllib.parse.quote(decoded_filename)
            response['Content-Disposition'] = 'attachment; filename="' + quoted_filename + '"'
            return response
        return 'not found'
    else:
        return HttpResponse('Error get Error')
    

def progress(request):
    if request.method == 'GET' and 'progress' in request.GET:
        global currentProgress
        letCurrentProgress = currentProgress
        currentProgress = 0
        return HttpResponse(letCurrentProgress)
    else:
        return HttpResponse('Error get')