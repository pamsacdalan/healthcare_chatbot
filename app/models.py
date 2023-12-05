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

class Dentist_Schedule(models.Model):
    clinic_id = models.IntegerField(null = True),
    user_id  = models.IntegerField(null = True),
    appointment_date  = models.DateField(null = True),
    start = models.IntegerField(null = True),
    stop = models.IntegerField(null = True),

    class Meta:
        db_table = 'app_dentist_schedule'

class UserAddress(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=True, to_field='username')
    city = models.CharField(max_length=1000)
