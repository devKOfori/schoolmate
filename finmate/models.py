from django.db import models

# Create your models here.

class PaymentFrequency(models.Model):
    # eg. Daily, Weekly, Monthly, Quarterly, Annually
    name = models.CharField(max_length=255)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    description = models.TextField(null=True)

    def __str__(self):
        return self.name
