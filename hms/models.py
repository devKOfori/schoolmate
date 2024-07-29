from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.


class Gender(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=6)

    class Meta:
        db_table = "gender"
        verbose_name_plural = "Genders"

    def __str__(self):
        return self.name


class Nationality(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "nationality"
        verbose_name_plural = "Nationalities"

    def __str__(self):
        return self.name


class Country(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=255)

    class Meta:
        db_table = "country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class Region(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "region"
        verbose_name_plural = "Region"

    def __str__(self):
        return self.name


class City(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "city"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name
    


class Neighborhoods(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    city = models.ForeignKey(
        City,
        verbose_name=_("city"),
        on_delete=models.CASCADE,
        related_name="neighborhoods",
    )
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "neighborhoods"
        verbose_name = _("neighborhood")
        verbose_name_plural = _("neighborhoods")

    def __str__(self):
        return self.name


class MaritalStatus(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "maritalstatus"
        verbose_name_plural = "Marital Statusses"

    def __str__(self):
        return self.name


class Relation(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "relation"
        verbose_name_plural = "Relations"

    def __str__(self):
        return self.name
