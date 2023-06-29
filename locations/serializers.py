from rest_framework import serializers
from .models import Location
from followers.models import Follower


class LocationSerializer(serializers.ModelSerializer):

    
    posts_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    posts_count = serializers.ReadOnlyField()
    
    def get_location(self, obj):
        request = self.context['request']
        return request.user == obj.name
   
    
    class Meta:
        model = Location
        fields = [
            'name', 'address', 'followers_count', 'posts_count',
             'image_url'
        ]
        
        