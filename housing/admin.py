from django.contrib import admin
from .models import (
    Amenities, Hostels, HostelAmenities,
    HostelPhotos, RoomCategories, RoomTypes, 
    HostelRoomTypes, Reviews, Beds, BedTypes,
    Blocks, RoomBeds, Rooms, Floors, ApplicationStatus, Application, ApplicationHostel,
    Tenant, HousingOffer
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
admin.site.register(Rooms)
admin.site.register(BedTypes)
admin.site.register(Beds)
admin.site.register(Blocks)
admin.site.register(RoomBeds)
admin.site.register(Floors)
admin.site.register(ApplicationStatus)
admin.site.register(Application)
admin.site.register(ApplicationHostel)
admin.site.register(Tenant)
admin.site.register(HousingOffer)