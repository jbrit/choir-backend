from django.urls import path
from .views import RegisterUserView, ChangePasswordView, AccountActivation, PasswordResetView, PasswordResetConfirmView
from rest_framework_simplejwt import views as jwt_views

app_name = "core"

urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path("register/", RegisterUserView.as_view()),
    path('activate/<slug:uid>/<slug:token>/', AccountActivation.as_view(), name='activate'),
    path("change-password/", ChangePasswordView.as_view()),
    path("reset-password/", PasswordResetView.as_view()),
    path("reset-password-confirm/", PasswordResetConfirmView.as_view()),
]