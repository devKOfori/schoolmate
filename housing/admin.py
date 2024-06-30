from django.contrib import admin
from .models import (
    Amenities, Hostels, HostelAmenities,
    HostelPhotos, RoomCategories, RoomTypes, 
    HostelRoomTypes, Reviews
)

# Register your models here.
admin.site.register(Hostels)
admin.site.register(HostelPhotos)
admin.site.register(Amenities)
admin.site.register(HostelAmenities)
admin.site.register(RoomCategories)
admin.site.register(RoomTypes)
admin.site.register(HostelRoomTypes)
admin.site.register(Reviews)