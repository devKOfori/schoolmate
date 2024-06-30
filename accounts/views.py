from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages

def login(request):
    if request.method == "POST":
        email = request.POST.get("email", None)
        password = request.POST.get("password", None)
        print(email, password)
        if all([email, password]):
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid Credentials")
                return render(request, "account/login.html")
    else:
        return render(request, "account/login.html")
    
def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        if all([email, password, password2]) and password2==password:
            usermodel = get_user_model()
            _ = usermodel.objects.create_user(email, password)
            return redirect("login")
        else:
            messages.error(request, "Correct the errors and try again")
            return render(request, "account/register.html")
    else:
        return render(request, "account/register.html")
    
def logout_view(request):
    logout(request)
    return redirect("login")