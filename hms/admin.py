from django.contrib import admin
from .models import (
    City,
    Country,
    Region,
    Relation,
    Nationality,
    Neighborhoods,
    Gender,
    MaritalStatus,
)

admin.site.register(City)
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(Relation)
admin.site.register(Nationality)
admin.site.register(Neighborhoods)
admin.site.register(Gender)
admin.site.register(MaritalStatus)

# Register your models here.
