from django.shortcuts import HttpResponse
from django.http import JsonResponse
import urllib.parse, urllib.request
import os
from yt_dlp import YoutubeDL
currentProgress = "Donetest"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Create your views here.
def fetchdata(request):
    if request.method == 'POST':
        url = request.POST['get']
        ydl = YoutubeDL()
        ydl.cache.remove()
        r = ydl.extract_info(url, download=False)
        data = [{'formats': r['formats'], 'thumbnail' : r['thumbnail'], 'title' : r['title']}]
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
            global currentProgress, fetchFile
            if d['status'] == 'downloading':
                currentProgress = d['_percent_str']
                print(d['_percent_str'])
                return d['_percent_str']
            elif d['status'] == 'finished':
                fetchFile = d['filename']
                return True 


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
            'outtmpl': '/static/context/'+dlType+'/'+request.GET['format']+'/%(title)s.%(ext)s',
            'progress_hooks': [my_hook]
        }
        

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(['https://www.youtube.com/watch?v='+request.GET['dlId']])
            
        print(fetchFile)

        if (fetchFile):
            fetchFileMerge = fetchFile
            if 'merge' in request.GET:
                fetchFileMerge = fetchFile.replace('.f140.m4a', '')
                if dlext == 'mp4': 
                    fetchFileMerge = fetchFileMerge+".mp4"
            if 'ajax' in request.GET:
                filenamedl = fetchFileMerge
                filenamedl = filenamedl.replace('static\\context\\audio\\'+request.GET['format']+'\\', '')
                filenamedl = filenamedl.replace('static\\context\\video\\'+request.GET['format']+'\\', '')
                fileData = [
                    { "name": filenamedl, "path": fetchFileMerge},
                ]
                json_data = {"context": fileData}
                return JsonResponse(json_data, safe=False)
                                    
            with open(os.path.join(BASE_DIR+'/'+fetchFileMerge), 'rb') as f:
                filename = os.path.basename(f.name).split('/')[-1]
                data = f.read()
            response = HttpResponse(data, content_type='application/'+dlType+'.'+dlext+'')
            filename_bytes = filename.encode('utf8')
            decoded_filename = urllib.parse.unquote(filename_bytes.decode('utf-8'))
            quoted_filename = urllib.parse.quote(decoded_filename)
            response['Content-Disposition'] = 'attachment; filename="' + quoted_filename + '"'
            return response
        return 'not found '
    else:
        return HttpResponse('Error get dfg')
    

def progress(request):
    if request.method == 'GET' and 'progress' in request.GET:
        global currentProgress
        letCurrentProgress = currentProgress
        currentProgress = 0
        return HttpResponse(letCurrentProgress)
    else:
        return HttpResponse('Error get')