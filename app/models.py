from django.db import models

# Create your models here.

class Dentist(models.Model):
    dentist_name = models.CharField(max_length=10000)
    clinic_name = models.CharField(max_length=10000)
    clinic_address = models.CharField(max_length=10000)
    city_town = models.CharField(max_length=10000)
    province = models.CharField(max_length=1000)
    region = models.CharField(max_length=1000)
    zipcode = models.IntegerField()
    contact_number = models.CharField(max_length=10000)
    clinic_schedule = models.CharField(max_length=10000) 
