from django.db.models.signals import post_save
from django.dispatch import receiver
from posts.models import Post
from .models import Location


@receiver(post_save, sender=Post)
def create_location(sender, instance, created, **kwargs):
    if created:
        try:
            Location.objects.get(name=instance.name)
        except Location.DoesNotExist:
            Location.objects.create(name=instance.name)
            