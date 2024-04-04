from django.shortcuts import render
from .forms import EmployeeCreationForm
from .models import Employee
from accounts.models import CustomUser
from housing.forms import HostelEmployeeAllocForm
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
    for emp in employees:
        hostel_alloc = emp.hostel_alloc.order_by("-timestamp").first()
        if hostel_alloc:
            # emp.hostel = hostel_alloc.hostel
            emp.hostel_role = hostel_alloc.role
    role_assign_form = HostelEmployeeAllocForm()
    context = {
        "employees": employees,
        "role_assign_form": role_assign_form,
        "hostel_alloc": hostel_alloc
    }
    return render(request, "employee/list_employee.html", context)