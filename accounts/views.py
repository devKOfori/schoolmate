from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from employee.forms import EmployeeCreationForm
from employee.models import Employee
from .models import CustomUser
from housing import models as housing_models
from datetime import datetime
import utils
# Create your views here.

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("dashboard"))
            else:
                return render(request, "authentication/login.html", {"form": form, "error_message": "Invalid email or password"})
    else:
        form = LoginForm()
    return render(request, 'authentication/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect("login")

def register(request):
    creator = request.user.employee
    employee_form = EmployeeCreationForm()
    if request.method == "POST":
        employee_form = EmployeeCreationForm(request.POST)
        if employee_form.is_valid():
            role = employee_form.cleaned_data.get("role")
            password = employee_form.cleaned_data.get("password")
            # print(password)
            is_superuser = True if role.id == 1 else False
            is_staff = True if role.id == 1 else False
            user = CustomUser.objects.create_user(
                first_name = employee_form.cleaned_data.get("first_name"),
                last_name = employee_form.cleaned_data.get("last_name"),
                email = employee_form.cleaned_data.get("email"),
                username = employee_form.cleaned_data.get("email"),
                password = employee_form.cleaned_data.get("password"),
                is_superuser = is_superuser,
                is_staff = is_staff,
            )
            employee = employee_form.save(commit=False)
            employee.user = user
            if role.id == 2:
                employee.company_code = creator.company_code
                employee.created_by = creator
            employee.save()
            emp_hostel_alloc = assign_default_role(employee=employee, created_by=creator)
            utils.update_emp_info(employee=employee, hostel_id=emp_hostel_alloc.hostel.hostel_id)
            return redirect(reverse("dashboard"))
        return render(request, "authentication/register.html", {"employee_form": employee_form})
    else:
        return render(request, "authentication/register.html", {"employee_form": employee_form})
    
def assign_default_role(employee: Employee, created_by: Employee):
    # 1. Assign new employee to the hostel of the one who created the employee record
    # 2. Assign a default role to the created employee record
    DEFAULT_ROLE = housing_models.HostelRoles.objects.get(id=3)
    creator_hostel_alloc = housing_models.HostelEmployeeAlloc.objects.filter(employee_id=created_by.id).last()
    print(creator_hostel_alloc.hostel.id)
    hostel = creator_hostel_alloc.hostel
    employee_hostel_alloc = housing_models.HostelEmployeeAlloc(
            hostel = hostel,
            employee = employee,
            role = DEFAULT_ROLE, 
            timestamp = datetime.now(),
            added_by = created_by
        )
    # print(employee_hostel_alloc)
    employee_hostel_alloc.save()
    return employee_hostel_alloc     
