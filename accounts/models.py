from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=100)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=10, blank=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(('email address'), unique=True)

    
class BlacklistedToken(models.Model):
    token = models.CharField(max_length=512)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('token', 'user')
