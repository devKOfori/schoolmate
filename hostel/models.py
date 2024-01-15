from django.db import models

# Create your models here.

class Hostel(models.Model):
    hostel_name = models.CharField(max_length = 255, db_index=True)
    address = models.TextField(blank=True)
    capacity = models.PositiveBigIntegerField(default = 0)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=255)
    establishment_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    rules_and_regulations = models.TextField(blank=True)

    class Meta:
        db_table = "hostels"
        verbose_name = "Hostel"
        verbose_name_plural = "Hostels"

    def __str__(self) -> str:
        return self.hostel_name
    

class HostelPhoto(models.Model):
    hostel_id = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    hostel_photo = models.ImageField(upload_to="images/%Y/%m/%d", null=True, blank=True)

    class Meta:
        db_table = "hostelphotos"
        verbose_name="Hostel Photo"
        verbose_name_plural="Hostel Photos"

    def __str__(self):
        return self.hostel_photo
    

class HostelFloor(models.Model):
    floor_number = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=255)

    class Meta:
        db_table = "hostelfloors"
        verbose_name="Hostel Floor"
        verbose_name_plural="Hostel Floor"

    def __str__(self):
        return self.floor_number
    

class HostelFacility(models.Model):
    facility_name = models.CharField(max_length=255)
    cost = models.PositiveBigIntegerField(default=0)
    description = models.TextField(max_length=255)

    class Meta:
        db_table = "roomfacilities"
        verbose_name="Room Facility"
        verbose_name_plural="Room Facilities"

    def __str__(self):
        return self.facility_name

class RoomType(models.Model):
    type_name = models.CharField(max_length=255)
    capacity = models.PositiveBigIntegerField(default=0)
    cost = models.PositiveBigIntegerField(default=0)
    description = models.TextField(blank=True)
    facilities = models.ManyToManyField(HostelFacility)

    class Meta:
        db_table = "roomtypes"
        verbose_name="Room Type"
        verbose_name_plural="Room Types"

    def __str__(self):
        return self.type_name


class RoomStatus(models.Model):
    status_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        db_table = "roomstatus"
        verbose_name="Room Status"
        verbose_name_plural="Room Statuses"

    def __str__(self):
        return self.status_name    


class Room(models.Model):
    room_number = models.CharField(max_length=255)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    floor = models.ForeignKey(HostelFloor, on_delete=models.SET_NULL, null=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey(RoomStatus, on_delete=models.SET_NULL, null=True)
    beds_count = models.PositiveBigIntegerField(default=1)
    room_area = models.CharField(max_length=255, blank=True)
    additional_facilities = models.ManyToManyField(HostelFacility, on_delete=models.SET_NULL)

    class Meta:
        db_table = "room"
        verbose_name="Room"
        verbose_name_plural="Rooms"

    def __str__(self):
        return self.room_number  