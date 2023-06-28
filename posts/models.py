from django.db import models
from django.contrib.auth.models import User
from locations.models import Location



class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_post_rgq6aq', blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'


def save(self, *args, **kwargs):
    if not self.id:
        location, _ = Location.objects.get_or_create(name=self.name)
        self.location = location
    super().save(*args, **kwargs)