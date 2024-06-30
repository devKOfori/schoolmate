from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name = "email address",
        max_length = 255,
        unique = True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = "customuser"

    def __str__(self):
        return self.email
    

class Gender(models.Model):
    name = models.CharField(max_length=6)

    def __str__(self):
        return self.name

class Nationality(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField(max_length=255)
    country_code = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class MaritalStatus(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Relation(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name