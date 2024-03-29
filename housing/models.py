from django.db import models
from employee.models import Employee
from school.models import (
    Nationality, Region, City, Gender,
    Country
)
from datetime import date, datetime
from finmate.models import PaymentFrequency
from django.utils import timezone
from accounts.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
import os
# Create your models here.

class VericationDocumentType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class VendorType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class HostelVendor(models.Model):
    vendor_id = models.CharField(max_length=255, unique=True, db_index=True)
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255, blank=True)
    vendor_type = models.ForeignKey(VendorType, on_delete=models.SET_NULL, null=True) # e.g., Individual, Company
    is_verified = models.BooleanField(default=False)
    registration_number = models.CharField(max_length=50)
    registration_date = models.DateField()
    registration_authority = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    cancellation_policy = models.TextField(blank=True, null=True)
    house_rules = models.TextField(blank=True, null=True)
    payment_details = models.ForeignKey("PaymentDetail", on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            employee = Employee.objects.get(id=self.created_by.id)
            employee.company_code = self.vendor_id
            employee.save()
        except ObjectDoesNotExist:
            pass

class PropertyType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

def upload_to(instance, filename):
    date_dir = f"{date.today().year}{str(date.today().month).zfill(2)}{str(date.today().day).zfill(2)}"
    new_filename = f"{instance.application_id}_document_{filename}"
    upload_destination = os.path.join("verification_document", date_dir, new_filename)
    return upload_destination

class VerifyProperty(models.Model):
    property_type = models.ForeignKey(PropertyType, on_delete=models.SET_NULL, null=True)
    application_id = models.CharField(max_length=255) # this field is used to store the ID of the application to which this document is attached
    verification_document_type = models.ForeignKey(
        VericationDocumentType, on_delete=models.SET_NULL, null=True
    )
    attachment = models.FileField("Attach Document", upload_to=upload_to)
    upload_date = models.DateTimeField(auto_now_add=True)
    upload_by = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    verifypropertyinfo = models.TextField(blank=True)
    property_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.application_id
    
class DocumentVerificationStatus(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class UpdateDocumentVerification(models.Model):
    updatedocumentverification_id = models.CharField(max_length=255, unique=True, db_index=True)
    verify_property = models.ForeignKey(
        VerifyProperty, on_delete = models.CASCADE
    )
    verification_status = models.ForeignKey(
        DocumentVerificationStatus, 
        on_delete=models.SET_NULL, 
        null=True
    )
    date_of_update = models.DateField(default=timezone.now)
    updated_by = models.ForeignKey(
        Employee, on_delete=models.DO_NOTHING,
    )
    updated_on = models.DateTimeField(auto_now_add=True)
    last_update_message = models.CharField(max_length=255)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.verify_property.application_id} - {self.verification_status.name}"

    def save(self, *args, **kwargs):
        super.save(*args, **kwargs)
        verify_property = self.verify_property
        if self.verification_status == "Approved":
            verify_property.property_verified = True
            verify_property.save()

class PaymentDetail(models.Model):
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)  # e.g., Bank transfer, PayPal, Mobile Money
    method_details = models.CharField(max_length=255)  # e.g., Bank account number, PayPal ID
    payment_terms = models.TextField(blank=True, null=True)
    currency_preference = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.payment_method} - {self.method_details}"

class Block(models.Model):
    hostel = models.ForeignKey("Hostel", on_delete=models.CASCADE)
    block_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name
    
class HostelStatus(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class HostelAmenities(models.Model):
    # eg. Gym, Laundry Room, TV Room
    name = models.CharField(max_length=255)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name

class Floor(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    floor_id = models.CharField(max_length=255, unique=True, db_index=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name

class Hostel(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    hostel_id = models.CharField(max_length=255, unique=True) # unique code assigned to each hostel
    location = models.CharField(max_length=255)
    capacity = models.PositiveBigIntegerField(default=0)
    warden = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True, null=True)
    registration_number = models.CharField(max_length=255, blank=True)
    date_established = models.DateField(default=date.today)
    company = models.CharField(max_length=255)
    status = models.ForeignKey(HostelStatus, on_delete=models.SET_NULL, null=True)
    amenities = models.ManyToManyField(HostelAmenities)
    vendor = models.ForeignKey(HostelVendor, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name="hostels")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        block = None
        if not Block.objects.filter(block_id=self.hostel_id).exists():
            block = Block.objects.create(hostel = self, block_id = self.hostel_id, name = self.name)
        if not Floor.objects.filter(floor_id=self.hostel_id).exists():
            Floor.objects.create(block=block, name=self.name, floor_id=self.hostel_id)

    def assign_warden(self, employee):
        self.warden = employee
        self.save()

    def __str__(self):
        return self.name
    
    
class Address(models.Model):
    hostel = models.OneToOneField(Hostel, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    street = models.CharField(max_length=255, blank=True)
    digital_address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.hostel} - {self.street}"
    
class HostelPhotos(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name="photos")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="photos/hostels/%Y/%m/%d")

    def __str__(self):
        return self.title
    
class RoomType(models.Model):
    # e.g., single, double, shared, dormitory
    name = models.CharField(max_length=255)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name
    
class RoomStatus(models.Model):
    # e.g., clean, under maintenance, needs repair
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class OccupancyStatus(models.Model):
    # e.g., completely occupied, partially occupied, empty
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class FacilityCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Facility(models.Model):
    name = models.CharField(max_length=255)
    facility_category = models.ForeignKey(FacilityCategory, on_delete=models.SET_NULL, null=True, blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=255, db_index=True, unique=True)
    block = models.ForeignKey(Block, on_delete=models.SET_NULL, null=True, blank=True)
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, null=True, blank=True)
    capacity = models.PositiveIntegerField(default=0)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_DEFAULT, default=1)
    room_status = models.ForeignKey(RoomStatus, on_delete=models.SET_DEFAULT, default=1)
    occupancy_status = models.ForeignKey(OccupancyStatus, on_delete=models.SET_NULL, null=True)
    facilities = models.ManyToManyField(Facility, blank=True)
    number_of_beds = models.PositiveBigIntegerField(default=1)
    availability_date = models.DateTimeField(default=timezone.now)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_number
    
class Tenant(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class RequestStatus(models.Model):
    # eg. Pending, Room Offered, Room Accepted, Cancelled, Room Rejected
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class RoomOfferStatus(models.Model):
    # eg. Pending, Accepted, Rejected, Withdrawn
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class RoomRequest(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True)
    request_id = models.CharField(max_length=255, unique=True, db_index=True)
    tenant_name = models.CharField(max_length=255)
    tenant_email = models.EmailField()
    tenant_phone = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True, blank=True)
    preferred_hostels = models.ManyToManyField(Hostel, blank=True)
    # preferred_blocks = models.ManyToManyField(Block)
    # preferred_floors = models.ManyToManyField(Floor)
    preferred_amenities = models.ManyToManyField(HostelAmenities, blank=True)
    preferred_room_types = models.ManyToManyField(RoomType, blank=True)
    preferred_facilities = models.ManyToManyField(Facility, blank=True)
    number_of_beds_required = models.PositiveIntegerField(default=1)
    move_in_date_earliest = models.DateTimeField("Move In Date (Earliest By)", null=True, blank=True)
    move_in_date_latest = models.DateTimeField("Move In Date (Latest By)", null=True, blank=True)
    duration_of_stay = models.PositiveIntegerField(blank=True, null=True)
    min_budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    preferred_payment_frequency = models.ForeignKey(PaymentFrequency, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    request_status = models.ForeignKey(RequestStatus, on_delete=models.SET_DEFAULT, default=1)

    def get_preferences(self):
        preferences = {
            "hostels": list(self.preferred_hostels.all()),
            "amenities": list(self.preferred_amenities.all()),
            "room_types": list(self.preferred_room_types.all()),
            "facilities": list(self.preferred_facilities.all()),
            "number_of_beds": self.number_of_beds_required,
            "min_budget": self.min_budget,
            "max_budget": self.max_budget,
            "duration_of_stay": self.duration_of_stay,
            "move_in_date_earliest": self.move_in_date_earliest,
            "move_in_date_latest": self.move_in_date_latest
        }
        
        preferences = {key: value for key, value in preferences.items() if value}
        
        return preferences

    def __str__(self):
        return self.request_id
    
class RoomOffer(models.Model):
    room_request = models.ForeignKey(RoomRequest, on_delete=models.SET_NULL, null=True)    
    offer_number = models.CharField(max_length=255, unique=True, db_index=True)
    # rooms_offered = models.ManyToManyField(Room)
    rooms_offered_new = models.ManyToManyField(Room, through="RoomOfferDetails")

    def __str__(self):
        return self.offer_number

class RoomOfferDetails(models.Model):
    room_offer = models.ForeignKey(RoomOffer, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_offered = models.DateTimeField(auto_now_add=True)
    offer_status = models.ForeignKey(RoomOfferStatus, on_delete=models.SET_NULL, null=True)
    valid_until = models.DateTimeField(blank=True, null=True)
    comment= models.TextField(blank=True)
    offered_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ("room_offer", "room")

    def __str__(self):
        return f"{self.room_offer} - {self.room}"

class OfferResponse(models.Model):
    # eg. Pending, Accepted, Rejected
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class RoomOfferResponse(models.Model):
    roomofferresponse_number = models.CharField(max_length=255)
    offer_number = models.ForeignKey(RoomOffer, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    offer_response = models.ForeignKey(OfferResponse, on_delete=models.SET_NULL, null=True)
    response_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)
    rent_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.roomofferresponse_number

class AssignmentUpdateType(models.Model):
    # eg. assigned (default), renewed, terminated,
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class AssignmentUpdate(models.Model):
    assignment = models.ForeignKey(
        "TenantRoomAssignment", on_delete=models.CASCADE
    )
    updated_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    update_type = models.ForeignKey(AssignmentUpdateType, on_delete=models.SET_DEFAULT, default=1)
    comment = models.TextField()
    original_start_date = models.DateTimeField()
    original_end_date = models.DateTimeField(null=True, blank=True)
    original_termination_date = models.DateTimeField(null=True, blank=True)
    new_start_date = models.DateTimeField()
    new_end_date = models.DateTimeField(null=True, blank=True)
    new_termination_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.assignment} - [{self.update_type}]"
    
class TenantRoomAssignment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    termination_date = models.DateTimeField(null=True, blank=True)
    assignment_status = models.ForeignKey(AssignmentUpdateType, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.tenant} - {self.room.hostel}, {self.room}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        room = self.room
        partially_occupied = completely_occupied = None
        try:
            partially_occupied = OccupancyStatus.objects.get(name="Partially Occupied")
            completely_occupied = OccupancyStatus.objects.get(name="Fully Occupied")
        except OccupancyStatus.DoesNotExist:
            # Handle the case where occupancy status objects don't exist
            pass

        if partially_occupied and completely_occupied:
            current_assignment_count = room.tenantroomassignment_set.filter(
                Q(end_date__isnull=True) | Q(end_date__gt=timezone.now())
            ).count()
            print(current_assignment_count)
            if current_assignment_count < room.capacity:
                room.occupancy_status = partially_occupied
            elif current_assignment_count == room.capacity:
                room.occupancy_status = completely_occupied

            room.save()
    
    def update_assignment(self, update_type, new_start_date, new_end_date=None, new_termination_date=None, updated_by=None, comment=None):
        if updated_by:
            AssignmentUpdate.objects.create(
                assignment=self,
                updated_by=updated_by,
                update_type=update_type,
                comment=comment,
                original_start_date=self.start_date,
                original_end_date=self.end_date,
                original_termination_date=self.termination_date,
                new_start_date=new_start_date,
                new_end_date=new_end_date,
                new_termination_date=new_termination_date
            )
        self.start_date = new_start_date
        self.end_date = new_end_date
        self.termination_date = new_termination_date
        self.assignment_status = update_type
        self.save()
