from django.db import models

# Create your models here.

class Dentist(models.Model):
    dentist_name = models.CharField(max_length=1000)