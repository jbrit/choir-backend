from django.urls import path, include
from rest_framework import routers
from .views import SongViewSet

app_name = "songs"

router = routers.DefaultRouter()
router.register(r"", SongViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
