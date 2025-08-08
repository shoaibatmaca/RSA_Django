from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


SUBSCRIPTION_CHOICES = [
    ('free', 'Free'),
    ('premium', 'Premium'),
    ('platinum', 'Platinum'),
]

class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class UserProfiles(models.Model):
    USER_ROLES = [
        ('admin', 'Admin'),
        ('analyst', 'Analyst'),
        ('user', 'User'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/',  blank=True, null=True)
    subscription_status = models.CharField(max_length=20, choices=SUBSCRIPTION_CHOICES, default='free')
    state = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=20, choices=USER_ROLES, default='user')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

