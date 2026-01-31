from django.shortcuts import render
from django.http import HttpResponse

def users(request):
    return HttpResponse("Here are the list of Users")

def signup(request):
    return render(request,"signup.html")
# Create your views here.
