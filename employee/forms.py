from django import forms
from .models import Employee


class EmployeeCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Employee
        exclude = [
            "photo", "department", "company_code",
            "emergency_contact", "is_active", 
            "employment_status", "hire_date", "marital_status",
            "user"
        ]