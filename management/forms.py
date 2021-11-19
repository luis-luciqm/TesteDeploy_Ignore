from typing import ClassVar
from django import forms
from django.db.models import fields
from django.forms import widgets
from django.forms.forms import Form
from .models import *
from django.forms.widgets import ClearableFileInput
from authentication.models import *

class StoreForm(forms.Form):
    name = forms.CharField(label='Insira o nome da Loja')
    url = forms.CharField(label='Insira a URL da Loja')
    logo = forms.ImageField(widget=ClearableFileInput) 
    banner = forms.ImageField(widget=ClearableFileInput) 

    class Meta:
        model = Store
        fields = ['name','url','logo','banner']
        
class StoreEditForm(forms.Form):
    name = forms.CharField(label='Insira o nome da Loja')
    url = forms.CharField(label='Insira a URL da Loja')
    active = forms.BooleanField(label='Active')
    logo = forms.ImageField(label='Logo', widget=ClearableFileInput)

    class Meta:
        model = Store
        fields = ['name','url','logo','active']

class UserEditForm(forms.Form):
    name = forms.CharField(label='Nome')
    email = forms.CharField(label='Email')
    phone = forms.CharField(label='phone')
    # roles = forms.IntegerField(required=)

    class Meta:
        model = User
        fields = ['name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={ 'placeholder': 'Insira seu Nome' }),
            'email': forms.TextInput(attrs={ 'placeholder': 'teste@gmail.com'}),
            'phone': forms.TextInput(attrs={ 'placeholder': '+55 (84) 9.9999-9999'})
        }