from django.db import models
from hms import models as hms_models
import uuid
from django.conf import settings
from django.utils.text import slugify
from utils.hostel_utils import generate_hostel_image_upload_path
# Create your models here.   


class Amenities(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField("Amenity", max_length=255, unique=True, db_index=True)

    class Meta:
        db_table = "amenities"
        verbose_name_plural = "Amenities"

    def __str__(self):
        return f"{self.name}"
    
class Hostels(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField("Hostel name", max_length=255, db_index=True)
    nameslug = models.SlugField(unique=True, blank=True, db_index=True)
    rating = models.FloatField(default=0)
    regNumber = models.CharField("Hostel Reg. Number", max_length=255, blank=True)
    
    address = models.CharField("Address", max_length=255)
    city = models.ForeignKey(
        hms_models.City, on_delete=models.SET_NULL,
        null=True, related_name="hostels",
        db_index=True
    )
    postalcode = models.CharField("Postal Code/Zip Code", max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True, null=True)

    amenities = models.ManyToManyField(
        Amenities, through="HostelAmenities",
        related_name="hostels"
    )

    room_types = models.ManyToManyField(
        "RoomTypes", related_name="hostels",
        through="HostelRoomTypes"
    )

    reviews = models.ManyToManyField(
        "Reviews", related_name="hostels"
    )

    createdby = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    datecreated = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hostels"
        verbose_name_plural = "Hostels"

    def save(self, *args, **kwargs):
        if not self.nameslug:
            slug = slugify(self.name)
            queryset = Hostels.objects.filter(nameslug=slug)
            counter = 1
            if queryset.exists():
                while queryset.exists():
                    self.nameslug = f'{slug}-{counter}'
                    counter += 1
                    queryset = Hostels.objects.filter(nameslug=self.nameslug)
            self.nameslug = slug
        super().save(*args, **kwargs)

class HostelAmenities(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    hostel = models.ForeignKey(Hostels, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenities, on_delete=models.CASCADE)
    description = models.CharField(blank=True)

    class Meta:
        db_table = "hostelamenities"
        verbose_name_plural = "Hostel Amenities"

    def __str__(self):
        return f"{self.hostel} - {self.amenity}"

class HostelPhotos(models.Model):
    hostel = models.ForeignKey(Hostels, on_delete=models.CASCADE, related_name="photos")
    title = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to=generate_hostel_image_upload_path)
    uploadedby = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True
    )
    dateuploaded = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hostelphotos"
        verbose_name_plural = "Hostel Photos"

    def __str__(self):
        return f"{self.photo}"

class RoomCategories(models.Model):
    # e.g., single, shared, family
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "roomcategories"
        verbose_name_plural = "Room Categories"

    def __str__(self):
        return f"{self.name}"   

class RoomTypes(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    category = models.ForeignKey(
        RoomCategories, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    room_type = models.CharField("Room Type", max_length=255, unique=True, db_index=True)

    class Meta:
        db_table = "roomtypes"
        verbose_name_plural = "Room Types"
    
    def __str__(self):
        return f"{self.room_type}"

class HostelRoomTypes(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    hostel = models.ForeignKey(
        Hostels, on_delete=models.CASCADE, related_name="roomtypes"
    )
    room_type = models.ForeignKey(
        RoomTypes, related_name="all_hostels", 
        on_delete=models.SET_NULL, null=True
    )
    number_of_rooms = models.PositiveIntegerField(default=1)
    number_of_beds = models.PositiveBigIntegerField(default=1)
    createdby = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True
    )
    datecreated = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hostelroomtypes"
        verbose_name_plural = "Hostel Room Types"

    def __str__(self):
        return f"{self.hostel} - {self.room_type}"

class Reviews(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    hostel = models.ForeignKey(
        Hostels, on_delete=models.CASCADE,
        related_name="all_reviews"
    )
    rating = models.IntegerField()
    comment = models.TextField()
    datecreated = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "reviews"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"{self.user} - {self.hostel} - {self.rating}"
