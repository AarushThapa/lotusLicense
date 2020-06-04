from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseServerError
from django.shortcuts import render,redirect
from . import forms
from .models import Log, Owner
from django.contrib import messages
from .camera import VideoCamera
from django.core.paginator import Paginator

def home(request):
    return render(request, 'home.html' , {'name':'Aarush'})


def displaylog(request):
    loglist = Log.objects.all()
    loglist = loglist.reverse()
    paginator = Paginator(loglist,50)
    page = request.GET.get('page')
    loglist = paginator.get_page(page)
    context = {
        'loglist': loglist,
        'ownerlist': Owner.objects.all()
    }
    return render(request,'displaylog.html',context)
# def ownerview(request):
#     context = {
#         'owners' : Owner.objects.all()
#     }
#     return render(request,'viewowners.html',context)


def addOwner(request):
    if request.method == "POST":
        form = forms.AddUser(request.POST)
        if form.is_valid():
            s = form.save(commit=False)
            s.added_by = request.user
            s.save()
            messages.success(request, 'Owner sucessfully added.')
            return redirect("addowner/")
    else:
        form = forms.AddUser()
    return render(request,'adduser.html',{'form':form})


def stream(request):
	return render(request, 'screen.html')

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@login_required
def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),content_type='multipart/x-mixed-replace; boundary=frame')



if __name__ == "__main__":
    video_feed()