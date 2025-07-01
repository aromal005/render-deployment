from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6,null=True,blank=True,)  

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class UserActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True,blank=True)
    path = models.CharField(max_length=100)
    method = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.method} {self.path}@ {self.created_at}"
    
class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Blog(BaseModel):
    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    