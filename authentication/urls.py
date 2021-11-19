from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (   TokenRefreshView,)


urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(),name='password-reset-complete'),
   
    path('modify-profile-image/', ModifyImageProfileViewSet.as_view(), name='modify-profile-image'),
    path('modify-profile-email/', ModifyEmailProfileViewSet.as_view(), name='modify-profile-email'),
    path('modify-profile-password/', UpdatePasswordViewSet.as_view(), name='modify-profile-password'),
    path('modify-profile-username/', UpdateUsernameViewSet.as_view(), name='modify-profile-password'),

    path('teste/',TesteRequest.as_view(),name="teste" )
]