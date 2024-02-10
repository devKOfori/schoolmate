from django.contrib import admin
from .models import (
    Employee, EmergencyContact, EmployeePosition,
    EmploymentStatus, EmploymentType, Address, Department
)
# Register your models here.
admin.site.register(Employee)
admin.site.register(EmergencyContact)
admin.site.register(EmployeePosition)
admin.site.register(EmploymentStatus)
admin.site.register(EmploymentType)
admin.site.register(Address)
admin.site.register(Department)