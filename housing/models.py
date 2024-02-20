from django.db import models
from employee.models import Employee
from school.models import Nationality, Region, City, Gender
from datetime import date, datetime
from user.models import CustomUser
from finmate.models import PaymentFrequency
from django.utils import timezone
# Create your models here.

class Block(models.Model):
    hostel = models.ForeignKey("Hostel", on_delete=models.CASCADE)
    block_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class HostelStatus(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class HostelAmenities(models.Model):
    # eg. Gym, Laundry Room, TV Room
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Floor(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    floor_id = models.CharField(max_length=255, unique=True, db_index=True)

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
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        block = None
        if not Block.objects.filter(block_id=self.hostel_id).exists():
            block = Block.objects.create(hostel = self, block_id = self.hostel_id, name = self.name)
        if not Floor.objects.filter(floor_id=self.hostel_id).exists():
            Floor.objects.create(block=block, name=self.name, floor_id=self.hostel_id)

    def __str__(self):
        return self.name
    
    
class Address(models.Model):
    hostel = models.OneToOneField(Hostel, on_delete=models.CASCADE)
    country = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True, blank=True)
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

    def __str__(self):
        return self.name
    
class RoomStatus(models.Model):
    # e.g., clean, under maintenance, needs repair
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
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=255, db_index=True)
    block = models.ForeignKey(Block, on_delete=models.SET_NULL, null=True, blank=True)
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, null=True, blank=True)
    capacity = models.PositiveIntegerField(default=0)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_DEFAULT, default=1)
    room_status = models.ForeignKey(RoomStatus, on_delete=models.SET_DEFAULT, default=1)
    facilities = models.ManyToManyField(Facility, blank=True)

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
    request_number = models.CharField(max_length=255, unique=True, db_index=True)
    tenant_name = models.CharField(max_length=255)
    tenant_email = models.EmailField()
    tenant_phone = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    preferred_hostels = models.ManyToManyField(Hostel)
    preferred_blocks = models.ManyToManyField(Block)
    preferred_floors = models.ManyToManyField(Floor)
    preferred_amenities = models.ManyToManyField(HostelAmenities)
    preferred_room_types = models.ManyToManyField(RoomType)
    preferred_facilities = models.ManyToManyField(Facility)
    number_of_beds_required = models.PositiveIntegerField(default=1)
    move_in_date_earliest = models.DateTimeField("Move In Date (Earliest By)")
    move_in_date_latest = models.DateTimeField("Move In Date (Latest By)")
    duration_of_stay = models.PositiveIntegerField(default=1)
    min_budget = models.DecimalField(max_digits=10, decimal_places=2)
    max_budget = models.DecimalField(max_digits=10, decimal_places=2)
    preferred_payment_frequency = models.ForeignKey(PaymentFrequency, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    request_status = models.ForeignKey(RoomStatus, on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return self.request_number
    
class RoomOffer(models.Model):
    room_request = models.ForeignKey(RoomRequest, on_delete=models.SET_NULL, null=True)    
    offer_number = models.CharField(max_length=255)
    date_offered = models.DateTimeField(auto_now_add=True)
    offer_status = models.ForeignKey(RoomOfferStatus, on_delete=models.SET_NULL, null=True)
    rooms_offered = models.ManyToManyField(Room)

    def __str__(self):
        return self.offer_number

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

class TenantRoomAssignment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.tenant} - {self.room.hostel}, {self.room}"
    

