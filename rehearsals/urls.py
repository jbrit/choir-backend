from django.urls import path
from rehearsals.views import RehearsalsView

app_name = "rehearsals"


urlpatterns = [
    path("", RehearsalsView.as_view()),
]
