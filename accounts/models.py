from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import UserManager


class User(AbstractBaseUser):

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    first_name = models.CharField(max_length=255 )

    middle_name = models.CharField(max_length=255,blank=True )

    last_name = models.CharField(max_length=255)

    email = models.EmailField(unique=True,max_length=255)

    image = models.ImageField( upload_to="profile_images/",blank=True,null=True )

    gender = models.CharField(max_length=10,choices=GENDER_CHOICES,blank=True,null=True)

    tc = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    is_admin = models.BooleanField( default=False )

    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True )

    updated_at = models.DateTimeField( auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "tc",
        "gender",
    ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin and self.is_active

    def has_module_perms(self, app_label):
        return self.is_admin and self.is_active

    @property
    def is_staff(self):
        return self.is_admin


class EmailOTP(models.Model):

    email = models.EmailField(  db_index=True )

    otp = models.CharField(max_length=6)

    purpose = models.CharField( max_length=30 )

    created_at = models.DateTimeField(auto_now_add=True)

    expires_at = models.DateTimeField()

    is_verified = models.BooleanField(default=False)

    attempts = models.PositiveIntegerField( default=0)

    def __str__(self):
        return f"{self.email} - {self.purpose}"