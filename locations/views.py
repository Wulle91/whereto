from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from whereto.permissions import IsOwnerOrReadOnly
from .models import Location
from .serializers import LocationSerializer


class LocationList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    queryset = Location.objects.annotate(
        posts_count=Count('name', distinct=True),
    ).order_by('-created_at')
    serializer_class = LocationSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    ordering_fields = [
        'posts_count',
        'location'
        'followers_count',
        
    ]
    
class LocationDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Location.objects.annotate(
        posts_count=Count('name', distinct=True),
        #followers_count=Count('name__followed', distinct=True),
    ).order_by('-created_at')
    serializer_class = LocationSerializer