from django.contrib import admin
from .models import (
    Facility, Hostel, Block, Floor,
    Address, HostelPhotos, RoomType, RoomStatus,
    FacilityCategory, Tenant, RequestStatus, RoomOfferStatus,
    RoomOfferResponse, RoomOffer, RoomRequest, OfferResponse, 
    TenantRoomAssignment, Room, HostelAmenities, HostelStatus,
    OccupancyStatus, VendorType, HostelVendor, PaymentDetail, 
    PaymentMethod, VericationDocumentType, PropertyType, 
    UpdateDocumentVerification, DocumentVerificationStatus
)
# Register your models here.
admin.site.register(VericationDocumentType)
admin.site.register(PropertyType)
admin.site.register(FacilityCategory)
admin.site.register(Facility)
admin.site.register(Hostel)
admin.site.register(Block)
admin.site.register(Floor)
admin.site.register(Address)
admin.site.register(HostelPhotos)
admin.site.register(RoomType)
admin.site.register(RoomStatus)
admin.site.register(Tenant)
admin.site.register(RequestStatus)
admin.site.register(RoomOfferStatus)
admin.site.register(RoomOfferResponse)
admin.site.register(RoomOffer)
admin.site.register(RoomRequest)
admin.site.register(OfferResponse)
admin.site.register(TenantRoomAssignment)
admin.site.register(Room)
admin.site.register(HostelStatus)
admin.site.register(HostelAmenities)
admin.site.register(OccupancyStatus)
admin.site.register(VendorType)
admin.site.register(HostelVendor)
admin.site.register(PaymentDetail)
admin.site.register(PaymentMethod)
admin.site.register(UpdateDocumentVerification)
admin.site.register(DocumentVerificationStatus)