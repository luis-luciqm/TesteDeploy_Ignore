from django.contrib.auth.views import LoginView
from django.http import HttpRequest
from django.views.generic.edit import CreateView
from .forms import UsuarioForm
from django.contrib import messages
from rolepermissions.mixins import HasRoleMixin
from rolepermissions.roles import assign_role
from django.conf import settings

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, PasswordChangeView

class UserLogin(LoginView):
    template_name = 'accounts/login.html'
    success_url = '/gerenciamento/'


   
    def form_invalid(self, form):
        messages.error(self.request, 'Verifique se sua conta já foi liberada pelo Administrador')
        return super().form_invalid(form)


  
class UserCreateView(SuccessMessageMixin,CreateView):
    template_name= 'accounts/register.html'
    form_class = UsuarioForm
    success_url = '/accounts/login'
    success_message = "Usuário Cadastrado! Solicite o administrador a liberação."

   

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        user = form.save(commit=False)
        user.is_active=False
        user.save()
        assign_role(user,'funcionario')
      
        return super().form_valid(form)
        
class PasswordReset(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    html_email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    
   

class PasswordResetDone(SuccessMessageMixin, PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class PasswordResetConfirm(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = '/accounts/login'


class PasswordResetCompleteView(SuccessMessageMixin, PasswordResetCompleteView):
    success_message = 'Senha Alterada com sucesso!'
    template_name = 'accounts/login.html'


class PasswordChange(SuccessMessageMixin, PasswordChangeView):
    template_name = 'accounts/password-change.html'
    success_url = 'index'
    success_message = "Senha alterada com sucesso!"
  
    
