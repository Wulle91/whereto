from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name}'
    
