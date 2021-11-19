from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
import jwt
from drf_yasg import openapi
from django.conf import settings
from rolepermissions.roles import assign_role
from django.template import Context
from django.template.loader import get_template
from django.template.loader import render_to_string

from .serializers import *
from .renderers import UserRenderer
from .models import User
from .utils import Util
from django.http import HttpResponsePermanentRedirect
import os
from django.core.mail import EmailMultiAlternatives

class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        
        assign_role(user,'cliente')
       
        token = RefreshToken.for_user(user).access_token
        current_site = 'pechinchou.nadic.ifrn.edu.br'

        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        # Foi definido que não será necessário mandar e-mail para confirmação.    
        ##Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)



class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    def get(self, request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    
class TesteRequest(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
 
    def get(self,request):
        return Response({'teste': 'Successfully Acess!'}, status=status.HTTP_200_OK)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')
            
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            if user.auth_provider in ['google','facebook']:
                return Response({'error': 'Não é permitido recuperar a senha, pois sua conta é vinculada um rede social'}, status=status.HTTP_400_BAD_REQUEST) 
             
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink +"?redirect_url="+redirect_url
                           
            context = {
                 'url': absurl
             }
            email_subject = 'Redefinir a senha'
            plain_message = render_to_string('authentication/email_reset_password_client.html', context)


            msg = EmailMultiAlternatives(
             subject=email_subject,
                body=plain_message,
                from_email='pechinchouemail@gmail.com',
                to=[email,]
            )
            msg.attach_alternative(plain_message, 'text/html')
            msg.send()

            return Response({'success': 'Enviamos um e-mail para alterar a senha.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Não foi encontrado usuário com este e-mail.'}, status=status.HTTP_400_BAD_REQUEST)
        

# Precisamos definir a tela de resetar senha.
class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetByEmailNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')
                    
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'As senhas foram alteradas com sucesso.'}, status=status.HTTP_200_OK)

class ModifyImageProfileViewSet(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SetNewImageUserSerializer

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer= self.get_serializer(user,data=request.data,partial=True)
    
        if request.data:
            if serializer.is_valid():
                serializer.save()
                return Response({"image":f'{settings.ADMIN_URL}/media/{user.image}'})
            else:
                return Response({"error": serializer.errors})
        return Response({'success': False, 'message': 'Insira uma imagem válida'}, status=status.HTTP_400_BAD_REQUEST) # se o usuario não passar nada
       
class ModifyEmailProfileViewSet(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SetNewEmailUserSerializer
    queryset = User.objects.all()

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer= self.get_serializer(user,data=request.data,partial=True)
      
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"E-mail Alterada com Sucesso!"})
        else:
            return Response({"error": serializer.errors})

class UpdatePasswordViewSet(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password alterado com Sucesso!',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateUsernameViewSet(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class =  ChangeUsernameSerializer
    model = User
    
    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.username == serializer.data.get("old_username"):
                return Response({"old_username": ["Please enter your current username"]}, status=status.HTTP_400_BAD_REQUEST)
            
            elif serializer.data.get("old_username") == serializer.data.get("new_username"):
                return Response({"new_username": ["The new name is the same as the old"]}, status=status.HTTP_400_BAD_REQUEST)
            
            # set_password also hashes the password that the user will get
            self.object.username = serializer.data.get("new_username")
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Nome de Usuário alterado com Sucesso!',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)