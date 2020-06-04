from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Owner(models.Model):
    owner_name = models.CharField(max_length=200)
    owner_contact = models.IntegerField()
    owner_email = models.CharField(max_length=50)
    vehiclenumber = models.CharField(max_length=10)
    added_by =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.owner_name


class Log(models.Model):
    numberplate = models.CharField(max_length=200)
    timein = models.DateTimeField(auto_now_add=True)
    timeout = models.DateTimeField(auto_now_add=False,null=True,blank=True)

    def __str__(self):
        return self.numberplate

    def getTimeout(self):
        return self.timeout