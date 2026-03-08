from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    username = models.CharField(max_length=150)   # NOT unique

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    

class Address(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)

    phone = models.CharField(max_length=15)

    address = models.TextField()

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class OTP(models.Model):

    phone = models.CharField(max_length=15)

    otp = models.CharField(max_length=6)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone