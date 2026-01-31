from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Students

def home(request):
   S = Students.objects.all()
   return render(request,"home.html", {'S':S})

def create_view(request):
    return render(request, "create.html" )

def create_student(request):
    if request.method == "POST":
        s_id = request.POST.get("s_id")
        s_name = request.POST.get("s_name")
        s_dept = request.POST.get("s_dept")

        if s_id and s_name and s_dept:
            Students.objects.create(s_id=s_id, s_name=s_name, s_dept=s_dept)
            return redirect("/")
        return render(request, "create.html")

