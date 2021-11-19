from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Product,Comment, Report_Problem
from django.db import models


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','store', 'slug','created_at']
    search_fields = ('title', )
    list_filter = ('store','subcategory')
    

class CommentAdmin(admin.ModelAdmin):
    list_display = ['product','text','active','author']
        
class Report_ProblemAdmin(admin.ModelAdmin):
    list_display = ['product','type','date','checked']

admin.site.register(Product,ProductAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Report_Problem, Report_ProblemAdmin)