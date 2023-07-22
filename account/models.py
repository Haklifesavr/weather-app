# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    USER_ROLE = 'user'
    ADMIN_ROLE = 'admin'
    
    ROLE_CHOICES = (
        (USER_ROLE, 'Simple User'),
        (ADMIN_ROLE, 'Admin User'),
    )
    
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    login_count = models.PositiveIntegerField(default=0)
    roles = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER_ROLE)
    # username = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"] 