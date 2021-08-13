from django.http import HttpResponse
from django.shortcuts import render
def Home(request):
	return HttpResponse('this is home page of ATG')