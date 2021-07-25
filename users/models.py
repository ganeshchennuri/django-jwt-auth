from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom User Model extending Abstract User"""
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    
    USERNAME_FIELD = 'email' # setting email as default login field
    REQUIRED_FIELDS = [] #removing email from required REQUIRED_FIELDS
    
    def __str__(self):
        return self.name