from django import forms
from . import models

class AddUser(forms.ModelForm):
    class Meta:
        model = models.Owner
        fields = ['owner_name','owner_contact','owner_email','vehiclenumber']