
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, status, viewsets
from core.permissions import IsAdminOrReadOnly
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from songs.serializers import SongSerializer
from songs.models import Song
from django.conf import settings

User = get_user_model()


class SongsView(ListCreateAPIView):
    """
    Upload and list song view
    """
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = SongSerializer
    queryset = Song.objects.all()


class SingleSongView(RetrieveUpdateDestroyAPIView):
    """
    Single song view
    """
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = SongSerializer
    queryset = Song.objects.all()
    lookup_field = 'id'

    
class SongViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows songs to be viewed or edited.
    """
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = SongSerializer
    queryset = Song.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()

    def get_queryset(self):
        """
        This view should return a list of all the songs
        """
        return self.queryset.all()