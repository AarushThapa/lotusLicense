from django.contrib.auth import login, authenticate
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Registerform(UserCreationForm):
    user_email = forms.EmailField()
    user_contact = forms.CharField()
    class Meta:
        model = User
        fields = ["username","user_email","user_contact","password1","password2"]
        widgets={
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'user_email': forms.TextInput(attrs={'class': 'form-control'}),
            'user_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.TextInput(attrs={'class': 'form-control'}),
            'password2': forms.TextInput(attrs={'class': 'form-control'})

        }
