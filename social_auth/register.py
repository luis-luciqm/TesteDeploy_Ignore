
from django.contrib.auth import authenticate
from authentication.models import User
from rolepermissions.roles import assign_role
import random
from rest_framework.exceptions import AuthenticationFailed
from decouple import config
from authentication.serializers import UserSerializer

def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email[0].auth_provider:
           
            registered_user = authenticate(email=email, password=config('SOCIAL_SECRET'))
            if not registered_user:
                raise AuthenticationFailed(detail='Falha na autenticação. Tente logar novamente')

            serializer = UserSerializer(registered_user)
            return serializer.data

        else:
            raise AuthenticationFailed(
                detail='O usuário já está cadastrado. Por favor retorne a página de login.' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'username': generate_username(name), 'email': email,
            'password': config('SOCIAL_SECRET')}
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.fullname = name
        user.auth_provider = provider
        assign_role(user,'cliente')
        user.save()

        new_user = authenticate(email=email, password=config('SOCIAL_SECRET'))
        
        if not new_user:
             raise AuthenticationFailed(detail='Falha na autenticação. Tente logar novamente')
        
        serializer = UserSerializer(new_user)
        return serializer.data

