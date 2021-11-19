from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(GroupWhatsapp)

class MarginAdmin(admin.ModelAdmin):
    list_display = ['name']
    
admin.site.register(Margin, MarginAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_display = ['id']
admin.site.register(Message, MessageAdmin)