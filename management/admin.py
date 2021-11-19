from django.contrib import admin
from .models import *
# Register your models here.



@admin.register(Warning)
class Warning_admin(admin.ModelAdmin):
    list_display = ['id','name','message']
    class Media:
        js = ('assets/js/tinymce2.js',)
        
@admin.register(Promotion)
class Promotion_admin(admin.ModelAdmin):
    list_display = ['id','name_product','link','description']
    class Media:
        js = ('assets/js/tinymce.js',)
@admin.register(SubCategory)
class Sub_Categoria_Admin(admin.ModelAdmin):
    list_display=['name','category']
    list_filter = ["category"]


admin.site.register(Store)
admin.site.register(Category)
admin.site.register(Freight)
admin.site.register(Form_Payment)