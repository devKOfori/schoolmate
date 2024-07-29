from django.db import models
from hms import models as hms_models
import uuid
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from utils.hostel_utils import generate_hostel_image_upload_path, update_hostel_user
from utils.floor_utils import create_floor
from utils.block_utils import create_block
from typing import List, Dict, Tuple
from django.utils import timezone

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
        hms_models.City,
        on_delete=models.SET_NULL,
        null=True,
        related_name="hostels",
        db_index=True,
    )
    neighborhood = models.ForeignKey(
        hms_models.Neighborhoods,
        verbose_name=_("neighborhood"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="hostels",
    )
    postalcode = models.CharField("Postal Code/Zip Code", max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True, null=True)

    amenities = models.ManyToManyField(
        Amenities, through="HostelAmenities", related_name="hostels"
    )

    room_types = models.ManyToManyField(
        "RoomTypes", related_name="hostels", through="HostelRoomTypes"
    )

    reviews = models.ManyToManyField("Reviews", related_name="hostels", blank=True)

    createdby = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="hostel"
    )
    datecreated = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hostels"
        verbose_name_plural = "Hostels"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        print(self.pk)
        if not self.nameslug:
            slug = slugify(self.name)
            queryset = Hostels.objects.filter(nameslug=slug)
            counter = 1
            if queryset.exists():
                while queryset.exists():
                    self.nameslug = f"{slug}-{counter}"
                    counter += 1
                    queryset = Hostels.objects.filter(nameslug=self.nameslug)
            self.nameslug = slug
        hostel = super().save(*args, **kwargs)

        # if not is_new:
        if not is_new:
            print("I'm here...")
            block = self.create_block()
            if block:
                _ = self.create_floor(block=block)
            self.update_hostel_user()

    def __str__(self):
        return f"{self.name}"

    def create_block(self):
        block = Blocks.objects.create(
            hostel=self, name="Default Block", createdby=self.createdby
        )
        return block

    def create_floor(self, block):
        floor = Floors.objects.create(
            block=block, name="Default Floor", createdby=self.createdby
        )
        return floor

    def create_roomtypes(
        self, room_types: List[dict]
    ) -> List[Tuple["HostelRoomTypes", bool]]:
        response = [
            HostelRoomTypes.objects.get_or_create(**room_type)
            for room_type in room_types
        ]
        return response

    def create_roomtype(self, room_type: dict) -> Tuple["HostelRoomTypes", bool]:
        room_type["hostel"] = self
        return HostelRoomTypes.objects.get_or_create(**room_type)

    def update_hostel_user(self):
        HostelEmployees.objects.create(user=self.createdby, hostel=self)


class HostelEmployees(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hostel = models.ForeignKey(Hostels, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} working for {self.hostel}"

    class Meta:
        db_table = "hostelemployees"
        verbose_name = "Hostel Employee"
        verbose_name_plural = "Hostel Employees"


class Blocks(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    hostel = models.ForeignKey(
        Hostels,
        on_delete=models.CASCADE,
        related_name="blocks",
    )
    name = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=255, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    datecreated = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "blocks"
        verbose_name_plural = "Blocks"

    def __str__(self):
        return f"{self.name}"


class Floors(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    block = models.ForeignKey(
        Blocks,
        on_delete=models.CASCADE,
        related_name="floors",
    )
    name = models.CharField(max_length=255, db_index=True)
    description = models.CharField(max_length=255, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    datecreated = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "floors"
        verbose_name_plural = "Floors"

    def __str__(self):
        return f"{self.name}"


class HostelAmenities(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    hostel = models.ForeignKey(Hostels, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenities, on_delete=models.CASCADE)
    description = models.CharField(blank=True)
    createdby = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    datecreated = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)

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
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
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
    # id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "roomcategories"
        verbose_name_plural = "Room Categories"

    def __str__(self):
        return f"{self.name}"


class RoomTypes(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    category = models.ForeignKey(
        RoomCategories, on_delete=models.SET_NULL, null=True, blank=True
    )
    room_type = models.CharField("Room Type", max_length=255, unique=True)
    room_type_code = models.CharField(
        _("Code"), max_length=50, db_index=True, null=True, blank=True
    )

    class Meta:
        db_table = "roomtypes"
        verbose_name_plural = "Room Types"

    def __str__(self):
        if self.room_type_code:
            return f"{self.room_type_code}"
        return f"{self.room_type}"


class HostelRoomTypes(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    hostel = models.ForeignKey(
        Hostels, on_delete=models.CASCADE, related_name="roomtypes"
    )
    room_type = models.ForeignKey(
        RoomTypes, related_name="all_hostels", on_delete=models.SET_NULL, null=True
    )
    number_of_rooms = models.PositiveIntegerField(default=1)
    bed_per_room = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    createdby = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    datecreated = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "hostelroomtypes"
        verbose_name_plural = "Hostel Room Types"

    def __str__(self):
        return f"{self.hostel} - {self.room_type}"


class BedTypes(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    bed_type = models.CharField(max_length=255, db_index=True)

    def __str__(self):
        return f"{self.bed_type}"

    class Meta:
        db_table = "bedtypes"
        verbose_name = "Bed Type"
        verbose_name_plural = "Bed Types"


class Rooms(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    room_number = models.CharField(max_length=255, db_index=True)
    hostel = models.ForeignKey(Hostels, on_delete=models.CASCADE, related_name="rooms")
    floor = models.ForeignKey(
        Floors, on_delete=models.SET_NULL, null=True, related_name="rooms"
    )
    room_type = models.ForeignKey(HostelRoomTypes, on_delete=models.CASCADE)
    comment = models.TextField()
    datecreated = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.hostel} -{self.room_type} - {self.room_number}"

    class Meta:
        db_table = "rooms"
        verbose_name = "Room"
        verbose_name_plural = "Rooms"


class Beds(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    hostel = models.ForeignKey(Hostels, on_delete=models.CASCADE)
    bed_number = models.CharField(max_length=255, db_index=True)
    bed_type = models.ForeignKey(BedTypes, on_delete=models.CASCADE)
    comment = models.TextField()
    datecreated = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)
    is_assigned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.hostel} -{self.bed_type} - {self.bed_number}"

    class Meta:
        db_table = "beds"
        verbose_name = "Bed"
        verbose_name_plural = "Beds"


class RoomBeds(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    bed = models.ForeignKey(Beds, on_delete=models.CASCADE)
    comment = models.TextField()
    datecreated = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)


class Reviews(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews"
    )
    hostel = models.ForeignKey(
        Hostels, on_delete=models.CASCADE, related_name="all_reviews"
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


class ApplicationStatus(models.Model):
    id = models.UUIDField(_("Status ID"), primary_key=True, default=uuid.uuid4)
    name = models.CharField(_("Status"), max_length=50, unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = "applicationstatus"
        verbose_name = "application Status"
        verbose_name_plural = "application Statuses"


class Application(models.Model):
    id = models.UUIDField(_("Application ID"), primary_key=True, default=uuid.uuid4)
    code = models.CharField(_("Application Code"), max_length=50, unique=True)
    tenant_name = models.CharField(_("Name of Applicant"), max_length=255)
    email = models.EmailField(_("Email"), max_length=254)
    phone = models.CharField(_("Phone"), max_length=255)
    application_date = models.DateTimeField(_("Application Date"), default=timezone.now)
    hostels = models.ManyToManyField(
        Hostels,
        verbose_name=_("hostels"),
        related_name="applications",
        through="ApplicationHostel",
    )

    def __str__(self):
        return str(self.code)

    class Meta:
        db_table = "applications"
        verbose_name = _("hostel Application")
        verbose_name_plural = _("hostel Applications")


class ApplicationHostel(models.Model):
    id = models.UUIDField(_("Application ID"), primary_key=True, default=uuid.uuid4)
    code = models.CharField(_("Application Code"), max_length=50)
    application = models.ForeignKey(
        Application, verbose_name=_("applications"), on_delete=models.CASCADE
    )
    hostel = models.ForeignKey(
        Hostels, verbose_name=_("hostels"), on_delete=models.CASCADE
    )
    room_types = models.ForeignKey(
        RoomTypes, verbose_name=_("room types"), on_delete=models.SET_NULL, null=True
    )
    status = models.ForeignKey(
        ApplicationStatus,
        verbose_name=_("status"),
        on_delete=models.SET_NULL,
        null=True,
        related_name="applications"
    )

    def __str__(self):
        return str(self.code)

    class Meta:
        db_table = "applicationhostel"
        verbose_name = "application Hostel"
        verbose_name_plural = "applications Hostels"
