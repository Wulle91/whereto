from django.db import models
from django.contrib.auth.models import User
from locations.models import Location



class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.ForeignKey(Location, on_delete=models.CASCADE)
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
        created = self.pk is None  # Check if the Post is being created or updated
        super().save(*args, **kwargs)
        if created:
            # Create a Location instance with the same name as the Post
            Location.objects.create(name=self.name, address='', image_url='')