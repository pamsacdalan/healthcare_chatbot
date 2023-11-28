from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Dentist(models.Model):
    dentist_name = models.CharField(max_length=10000,null = True)
    clinic_name = models.CharField(max_length=10000,null = True)
    clinic_address = models.CharField(max_length=10000,null = True)
    city_town = models.CharField(max_length=10000,null = True)
    province = models.CharField(max_length=1000,null = True)
    region = models.CharField(max_length=1000,null = True)
    zipcode = models.IntegerField(null = True)
    contact_number = models.CharField(max_length=10000,null = True)
    clinic_schedule = models.CharField(max_length=10000,null = True) 

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null = True)
    message = models.TextField(null = True)
    response = models.TextField(null = True)
    created_at = models.DateTimeField(auto_now_add=True,null = True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'

class Clinic_Schedule(models.Model):
    clinic_id = models.IntegerField(),
    user_id  = models.IntegerField(),
    day  = models.IntegerField(),
    start = models.IntegerField(),
    stop = models.IntegerField(),