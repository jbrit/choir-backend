from rest_framework import generics
from core.permissions import IsAdminOrReadOnly
from rehearsals.models import Rehearsal
from rehearsals.serializers import RehearsalSerializer


class RehearsalsView(generics.ListCreateAPIView):
    queryset = Rehearsal.objects.all()
    serializer_class = RehearsalSerializer
    permission_classes = (IsAdminOrReadOnly,)
