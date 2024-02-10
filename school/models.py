from django.db import models

# Create your models here.

class Gender(models.Model):
    name = models.CharField(max_length=6)

    def __str__(self):
        return self.name

class Nationality(models.Model):
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
    
