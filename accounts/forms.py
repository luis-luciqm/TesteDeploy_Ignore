
from authentication.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class UsuarioForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['email', 'username','fullname', 'password1', 'password2']