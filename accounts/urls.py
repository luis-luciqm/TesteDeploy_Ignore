  
from django.urls import path, include
from .views import UserLogin, UserCreateView, PasswordReset, \
PasswordResetConfirm, PasswordResetCompleteView, PasswordChange, PasswordResetDone
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('accounts/login/', UserLogin.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/criar/', UserCreateView.as_view(), name='criar_conta'),
    path('accounts/password_reset/', PasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', PasswordChange.as_view(), name='password-change'),
    # path('accounts/password_reset_done/', )
]