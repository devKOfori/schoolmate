from typing import Any
from django import forms
from .models import Tenant

class TenantCreationForm(forms.ModelForm):
    class Meta:
        model = Tenant
        exclude = ["user", "email"]

    

    