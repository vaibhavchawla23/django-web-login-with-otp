from django.db import models
from django.contrib.auth.models import AbstractUser
import random
import string
import uuid
# Create your models here.


class CustomUser(AbstractUser):
  is_doctor = models.BooleanField(default=False, editable=False)

class Doctor(CustomUser):
  Dept = models.CharField(blank=False,max_length=100)

class Patient(CustomUser):
  Age = models.IntegerField(blank=False)
  Height = models.IntegerField(blank=False)
  Weight = models.IntegerField(blank=False)

    
class Code(models.Model):
    number  = models.CharField(blank=True,max_length=6)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.number)
    
    def save(self, *args, **kwargs):
        hex_list = list(string.hexdigits)
        code_items=[]
        for i in range (6): 
            hex=random.choice(hex_list)
            code_items.append(hex) 
        code_string="".join(str(item) for item in code_items)
        print ("OTP Refreshed!", code_string)
        self.number=code_string
        super().save(*args, **kwargs)

class Appointment(models.Model):
    appointment_id = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=36)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    Dept = models.CharField(blank=True, null=True, max_length=20)