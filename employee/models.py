from django.db import models
from datetime import date
from django.utils import timezone
from . import defaults as df
from school.models import (
    Gender, Nationality, MaritalStatus, Relation
)
from user.models import CustomUser
# Create your models here.

class EmploymentType(models.Model):
    # full-time, part-time, temporary, contract, freelance, seasonal, and internship.
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class EmergencyContact(models.Model):
    emergency_contact_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    relation = models.ForeignKey(
        Relation,
        on_delete = models.SET_DEFAULT,
        default = df.EMERGENCY_CONTACT.get('PREFIX') + df.EMERGENCY_CONTACT.get('DEFAULT_VALUE')
    )

    def __str__(self):
        return self.emergency_contact_name

class EmploymentStatus(models.Model):
    # active, on leave, terminated, laid off, retired, and resigned.
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class EmployeePosition(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name
    

class Employee(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    employee_id = models.CharField(
        max_length=df.EMPLOYEE_ID.get('MAX_LENGTH'), 
        unique = df.EMPLOYEE_ID.get('UNIQUE')
    )
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(default=date.today)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True)
    marital_status = models.ForeignKey(MaritalStatus, on_delete=models.SET_NULL, null=True)
    hire_date = models.DateTimeField(default=timezone.now)
    employment_type = models.ForeignKey(
        EmploymentType, on_delete=models.SET_DEFAULT, 
        default = 1
    )
    employment_status = models.ForeignKey(
        EmploymentStatus, on_delete=models.SET_DEFAULT, 
        default=1
    )
    position = models.ForeignKey(EmployeePosition, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(null=True, blank=True)
    emergency_contact = models.ForeignKey(EmergencyContact, on_delete=models.SET_NULL, null=True, related_name='employees')
    is_active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='photos/employee/%Y/%m/%d', null=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Address(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE )
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    digital_address = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.street}'
    
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    head_of_department = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='department_head', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

