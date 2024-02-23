from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def dashboard(request):
    employee = request.user.employee
    print(employee)
    return render(request, "school/dashboard.html", {"employee": employee})