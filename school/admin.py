from django.contrib import admin
from .models import (
    Gender, MaritalStatus, Relation, Nationality, 
    Region, City, Country
)
# Register your models here.
admin.site.register(Gender)
admin.site.register(MaritalStatus)
admin.site.register(Relation)
admin.site.register(Nationality)
admin.site.register(Region)
admin.site.register(City)
admin.site.register(Country)