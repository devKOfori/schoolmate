from django.contrib import admin
from .models import (
    Facility, Hostel, Block, Floor,
    Address, HostelPhotos, RoomType, RoomStatus,
    FacilityCategory
)
# Register your models here.
admin.site.register(FacilityCategory)
admin.site.register(Facility)
admin.site.register(Hostel)
admin.site.register(Block)
admin.site.register(Floor)
admin.site.register(Address)
admin.site.register(HostelPhotos)
admin.site.register(RoomType)
admin.site.register(RoomStatus)
