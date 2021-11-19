from django.contrib import admin

# Register your models here.
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'auth_provider', 'created_at']
    search_fields = ('username','email','fullname')
    list_filter = ('auth_provider','groups')

admin.site.register(User, UserAdmin)
