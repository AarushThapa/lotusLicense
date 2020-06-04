from django.test import TestCase
from .models import Log
# Create your tests here.


def la():
	if "DL7C0T939" == Log.numberplate:
		print("hello")

la()
