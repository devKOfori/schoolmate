from django.shortcuts import render, redirect
from .forms import TenantCreationForm
from user.forms import UserCreationForm
from django.urls import reverse
# Create your views here.


def register(request):
    user_form = UserCreationForm(prefix="user")
    tenant_form = TenantCreationForm(prefix="tenant")
    if request.method == "POST":
        user_form = UserCreationForm(request.POST, prefix="user")
        tenant_form = TenantCreationForm(request.POST, prefix="tenant")
        if user_form.is_valid() and tenant_form.is_valid():
            user = user_form.save()
            tenant = tenant_form.save(commit=False)
            tenant.user = user
            tenant.email = user.email
            tenant.save()
            return redirect(reverse("login"))
        return render(request, "housing/tenant_creation.html", {"user_form": user_form, "tenant_form": tenant_form, "error_message": "Error somewhere"})
    else:
        return render(request, "housing/tenant_creation.html", {"user_form": user_form, "tenant_form": tenant_form})