from django.shortcuts import render
from .forms import EmployeeCreationForm
from .models import Employee
from accounts.models import CustomUser
# Create your views here.

def list_employee(request):
    employees = Employee.objects.all()
    context = {
        "employees": employees
    }
    return render(request, "employee/list_employee.html", context)

def my_employee(request):
    me = request.user.employee
    employees = Employee.objects.filter(created_by=me)
    context = {
        "employees": employees
    }
    return render(request, "employee/list_employee.html", context)