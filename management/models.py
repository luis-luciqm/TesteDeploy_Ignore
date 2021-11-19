from django.db import models
from django.utils.translation import activate
from authentication.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save

class Store(models.Model):
    STYLE_LINK_CHOICES = (
        ('I','Início'), 
        ('M', 'Meio'),
        ('F', 'Fim')
    )
    
    name = models.CharField('name',max_length=100)
    url = models.CharField('url', max_length=500)
    id_partner = models.CharField('id_partner', max_length=500, default='')
    style_link = models.CharField('style_link', max_length=100, choices=STYLE_LINK_CHOICES, default='I')
    active = models.BooleanField('active',default=True)
    logo = models.FileField(upload_to="img/store/%m/%d")
    slug = models.SlugField(blank=True)
    banner = models.FileField(upload_to='img/loja/banner',blank=True,null=True)
    primary_color = models.CharField('primary_color', max_length=50, default='#ffffff')
    
    class Meta:
        verbose_name="Loja"  

    def __str__(self) -> str:
        return self.name
    
def store_pre_save_receiever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
pre_save.connect(store_pre_save_receiever, sender=Store)    


class Category(models.Model):
    name = models.CharField('name', max_length=100)
    image = models.FileField(upload_to='img/category/image',blank=True,null=True)
    slug= models.SlugField(blank=True)
    banner = models.FileField(upload_to='img/category/banner',blank=True,null=True)

    def __str__(self) -> str:
        return  self.name   
    class Meta:
        verbose_name="Categoria"  
        ordering = ['name']

def category_pre_save_receiever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
pre_save.connect(category_pre_save_receiever, sender=Category)



class SubCategory(models.Model):
    name = models.CharField('name', max_length=100)
    category = models.ForeignKey(Category, related_name='subcategorys', on_delete=models.CASCADE, blank =True, null=True)
    image = models.FileField(upload_to='img/subcategory/image',blank=True,null=True)
    slug= models.SlugField(blank=True)

    def __str__(self) -> str:
        return  self.name 
    class Meta:
        verbose_name="Subcategoria"  
        ordering = ['name']

def subcategory_pre_save_receiever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
pre_save.connect(subcategory_pre_save_receiever, sender=SubCategory)

class Promotion(models.Model):
    name_product = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    description = models.TextField()
    
class Freight(models.Model):
    name = models.CharField('name', max_length=100)
    class Meta:
        verbose_name="Frete" 
    
    def __str__(self):
        return self.name
class Form_Payment(models.Model):
    name = models.CharField('name', max_length=100)
    class Meta:
        verbose_name="Forma de Pagamento" 
   
    def __str__(self):
        return self.name
class Warning(models.Model):
    name = models.CharField('name', max_length=100)
    message = models.TextField()
    class Meta:
        verbose_name="Aviso" 
    def __str__(self):
        return self.name