from re import VERBOSE
from django.db import models

# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
# Api use tokens
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):

    def create_user(self, username,email,password=None,fullname='',phone=''):
        if username is None:
            raise TypeError('Usuário deve informar o nome')
        if email is None:
            raise TypeError('Users deve informar o Email')
    
        user = self.model(username=username,fullname=fullname,email=self.normalize_email(email),phone=phone)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google','email': 'email'}


class User(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField('Nome Completo',max_length=255,db_index=True)
    username = models.CharField('Nome Usuário',max_length=255, db_index=True)
    phone =  models.CharField(max_length=50, db_index=True,null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    image = models.FileField(upload_to="imgUsers/%Y", null=True,blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    class Meta:
        verbose_name="Usuário" 