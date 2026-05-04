from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    matric_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    
    def __str__(self):
        return self.matric_number or self.username