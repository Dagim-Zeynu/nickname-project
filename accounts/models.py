from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile'
    )
    full_name = models.CharField(max_length=255)
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE,
        related_name='profiles'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    registration_complete = models.BooleanField(default=False)
    
    def __str__(self):
        return self.full_name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'], 
                name='unique_user_profile'
            )
        ] 