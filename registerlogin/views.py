from __future__ import unicode_literals
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import Registerform



# Create your views here.
def register(request):
    if request.method == "POST":
        form = Registerform(request.POST)
        fields = '__all__'
        if form.is_valid():
            form.save()
            return redirect("login/")
    else:
        form = Registerform()
    return render(request, 'register.html',{"form":form})