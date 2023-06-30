from django.db import models
from django.contrib.auth.models import User
from locations.models import Location


class Follower(models.Model):
    owner = models.ForeignKey(
        User, related_name='following', on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        User, related_name='followed', on_delete=models.CASCADE
    )
    followed_location = models.ForeignKey(
        Location, related_name='followers', on_delete=models.CASCADE, default=None
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'followed', 'followed_location']

    def __str__(self):
        return f'{self.owner} {self.followed}'
