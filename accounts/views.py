from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.urls import reverse
from employee.forms import EmployeeCreationForm
from employee.models import Employee
from .models import CustomUser
from housing import models as housing_models
from datetime import datetime
import utils
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail

# Create your views here.

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                print(user, password)
                login(request, user)
                return redirect(reverse("dashboard"))
            else:
                messages.error(request, "Invalid email or password")
                return render(request, "authentication/login.html", {"form": form})
    else:
        form = LoginForm()
        return render(request, 'authentication/login.html', {'form': form, "hide_menu":True})

def user_logout(request):
    logout(request)
    return redirect("login")

def register(request):
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
                creator = request.user.employee
                employee.company_code = creator.company_code
                employee.created_by = creator
            employee.save()
            if role.id == 2:
                emp_hostel_alloc = assign_default_role(employee=employee, created_by=employee.created_by)
                utils.update_emp_info(employee=employee, hostel_id=emp_hostel_alloc.hostel.hostel_id)
            return redirect(reverse("login"))
        return render(request, "authentication/register.html", {"employee_form": employee_form})
    else:
        return render(request, "authentication/register.html", {"employee_form": employee_form})
    
def register_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if all([email, password, password2]) and password == password2:
            if not CustomUser.objects.filter(email=email).exists():
                user = CustomUser.objects.create_user(
                    email = email,
                    username = email,
                    password = password
                )
                return redirect("login")
            else:
                messages.error(request, "A user with this email already exist.")
                return render(request, 'authentication/register.html')
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, 'authentication/register.html')
    else:
        return render(request, 'authentication/register.html')
    
def assign_default_role(employee: Employee, created_by: Employee):
    # 1. Assign new employee to the hostel of the one who created the employee record
    # 2. Assign a default role to the created employee record
    DEFAULT_ROLE = housing_models.HostelRoles.objects.get(id=3)
    creator_hostel_alloc = housing_models.HostelEmployeeAlloc.objects.filter(employee_id=created_by.id).last()
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


# reset password view
def reset_password(request):
    if request.method =='POST':
        email = request.POST.get('email')
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            messages.error(request, 'Sorry, email address not found')
            return render(request, 'authentication/reset_password.html')

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        context = {
            'email':user.email,
            'domain': request.get_host(),
            'site_name': 'Your Site Name',
            'uid': uid,
            'user': user,
            'token': token,
            'protocol': 'https' if request.is_secure() else 'http',
        }
        email_template_name = 'authentication/reset_password_email.html'
        subject = 'Password reset'
        email_body = render_to_string(email_template_name, context)
        send_mail(
            subject=subject, message=email_body, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[user.email]
        )

        messages.success(request, "Password reset email has been sent")
        return render(request, 'authentication/reset_password.html')
    else:
        return render(request, 'authentication/reset_password.html')