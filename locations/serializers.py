from rest_framework import serializers
from .models import Location
from followers.models import Follower


class LocationSerializer(serializers.ModelSerializer):
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    posts_count = serializers.ReadOnlyField()
    is_following = serializers.SerializerMethodField()

    def get_location(self, obj):
        request = self.context['request']
        return Follower.objects.filter(
            owner=request.user, followed_location=obj).exists()

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            following = Follower.objects.filter(
                owner=request.user, followed_location=obj).first()
            return following is not None
        return False

    class Meta:
        model = Location
        fields = [
            'name', 'address', 'followers_count', 'posts_count',
            'image_url', 'is_following'
        ]
