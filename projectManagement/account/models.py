from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser
from account.manager import CustomUserManager


# User Model
class CustomUser(AbstractUser):
    # id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)
    # Custom manager
    objects = CustomUserManager()

    # Additional fields you can add
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Used for admin access
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # Email is used for login, instead of username
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


    def __str__(self):
        return self.username


