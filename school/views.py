from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.

def dashboard(request):
    try:
        employee = request.user.employee
        return render(request, "school/dashboard.html", {"employee": employee})
    except:
        return redirect(reverse("login"))
    
def index(request):
    return render(request, "school/index.html")