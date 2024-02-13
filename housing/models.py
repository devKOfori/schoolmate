from django.db import models
from employee.models import Employee
from school.models import Nationality, Region, City, Gender
from datetime import date
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

class Hostel(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    hostel_id = models.CharField(max_length=255) # unique code assigned to each hostel
    location = models.CharField(max_length=255)
    capacity = models.PositiveBigIntegerField(default=0)
    warden = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True, null=True)
    registration_number = models.CharField(max_length=255, blank=True)
    date_established = models.DateField(default=date.today)
    company = models.CharField(max_length=255)
    status = models.ForeignKey(HostelStatus, on_delete=models.SET_NULL, null=True)
    

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not Block.objects.filter(block_id=self.hostel_id).exists():
            Block.objects.create(hostel = self, block_id = self.hostel_id, name = self.name)

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

    
class Floor(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class RoomType(models.Model):
    # e.g., single, double, shared
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
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
    

