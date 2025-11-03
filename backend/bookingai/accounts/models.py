from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    USER_TYPES = [
        ('guest', 'Guest User'),
        ('host', 'Host User'),
        ('admin', 'Admin User'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='guest')