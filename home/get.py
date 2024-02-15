from django.shortcuts import render, HttpResponse
from django.urls import path, include
from django.http import JsonResponse
import urllib.parse, urllib.request
import os
from youtube_dl import YoutubeDL


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
        return HttpResponse('Error')
    

def downloadContext(request):
    if request.method == 'GET' and 'format' in request.GET:
        
        class MyLogger(object):
            def debug(self, msg):
                pass

            def warning(self, msg):
                pass

            def error(self, msg):
                print(msg)



        def my_hook(d):
            if d['status'] == 'downloading':
                return d['_percent_str']
            elif d['status'] == 'finished':
                print(d)
                global fetchFile
                fetchFile = d['filename']


        dlformat = request.GET['format']+'/best'
        dlext = request.GET['ext']
        dlType = 'video'
        if(request.GET['type'] == 'audio'):
            dlType = 'audio'

        ydl_opts = {
            'format': dlformat,
            'logger': MyLogger(),
            'outtmpl': '/context/'+dlType+'/'+request.GET['format']+'/%(title)s-%(id)s.%(ext)s',
            'progress_hooks': [my_hook],
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://www.youtube.com/watch?v='+request.GET['dlId']])

        
        if(fetchFile):
            with open(os.path.join(BASE_DIR+'/'+fetchFile), 'rb') as f:
                data = f.read()   
            filenamedl = fetchFile.replace('context\\audio\\'+request.GET['format']+'\\', '')
            filenamedl = filenamedl.replace('context\\video\\'+request.GET['format']+'\\', '')
            response = HttpResponse(data, content_type='application/'+dlType+'.'+dlext+'')
            response['Content-Disposition'] = 'attachment; filename="'+filenamedl+'"'
            return response
        return 'not found'
    else:
        return HttpResponse('Error')