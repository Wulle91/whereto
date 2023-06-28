from rest_framework import serializers
from .models import Location
from followers.models import Follower


class LocationSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='location.name')
    following_id = serializers.SerializerMethodField()
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    posts_count = serializers.ReadOnlyField()
    
    def get_location(self, obj):
        request = self.context['request']
        return request.user == obj.name
    
    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.name
            ).first()
            return following.id if following else None
        return None
    
    class Meta:
        model = Location
        fields = [
            'name', 'address', 'followers_count', 'posts_count',
            'following_id', 'image_url'
        ]