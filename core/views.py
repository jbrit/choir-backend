from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from core.models import Profile
from core.serializers.auth import RegisterUserSerializer, ChangePasswordSerializer, PasswordResetSerializer, \
    PasswordResetConfirmSerializer
from django.contrib.auth import get_user_model

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from core.serializers.biodata import BiodataSerializer
from core.serializers.tokens import account_activation_token, password_reset_token
from django.conf import settings

VERIFICATION_URL = settings.VERIFICATION_URL
PASSWORD_RESET_URL = settings.PASSWORD_RESET_URL

User = get_user_model()

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)


class RegisterUserView(GenericAPIView):
    """
    User Registration View accepting required fields
    and sending email for account activation
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Choir Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'url': VERIFICATION_URL
            })
            print(subject, message)
            # user.email_user(subject, message)
            data = {"message": "Please check your email to verify your account"}
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(data={"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AccountActivation(APIView):
    """
    User activation link is confirmed,
    therefore user's account is activated
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            uidb64 = kwargs.get('uid')
            token = kwargs.get('token')
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_verified = True
            user.save()
            return Response(data={"message": "Your account has been activated"}, status=status.HTTP_200_OK)
        return Response(data={"message": "Invalid or used token"}, status=status.HTTP_400_BAD_REQUEST)
       
class ChangePasswordView(GenericAPIView):
    """
    User Password Change View
    """
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, instance=self.request.user)
        if serializer.is_valid():
            serializer.update_password()
            return Response(data={"message": "Password has been changed successfully"}, status=status.HTTP_200_OK)
        return Response(data={"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(GenericAPIView):
    """
    User Reset View accepting email to send
    password reset details so as to reset password
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            current_site = get_current_site(request)
            subject = 'Reset your Choir Account Password'
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': password_reset_token.make_token(user),
                'url': PASSWORD_RESET_URL
            })
            user.email_user(subject, message)
            data = {"message": "Please check your email to reset your password"}
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(data={"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(GenericAPIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.
    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordResetConfirmView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password has been reset successfully."}, status=status.HTTP_200_OK
            )
        return Response(data={"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BiodataView(UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = BiodataSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user.id)