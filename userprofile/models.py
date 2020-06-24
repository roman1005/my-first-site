from django.db import models
from django.contrib.auth.models import User


class UserHomePage(models.Model):
    First_Name=models.CharField(max_length=50)
    Last_Name=models.CharField(max_length=50)
    Birth_Date = models.DateTimeField(blank=True, null=True)
    user_id = models.ForeignKey(User, models.deletion.CASCADE)
    Profile_Photo=models.ImageField( null=True, blank=True)
    Studied_at=models.TextField(max_length=1000, null=True, blank=True)
    Adress=models.CharField(max_length=200, null=True, blank=True)
    Mobile_Phone=models.CharField(max_length=1000, null=True, blank=True)
    Current_Workplace=models.CharField(max_length=100, null=True, blank=True)
    Worked_at=models.TextField(max_length=1000, null=True, blank=True)
    Hobbies=models.TextField(max_length=2000)


# Create your models here.
