from django.db import models
from django.utils import tree
from django.utils.text import slugify
from authentication.models import User
from management.models import SubCategory, Store,Freight,Warning,Form_Payment
from django.db.models.signals import post_save, pre_save
import os

from django.core.files.temp import NamedTemporaryFile
from PIL import Image
from django.core.files import File

from product.utils import unique_slug_generator
from django.core.cache import cache
from ckeditor.fields import RichTextField

class Teste(models.Model):
    nome = models.CharField(max_length=250)
    cpf = models.CharField(max_length=25)

class Product(models.Model):
      # Status Choice
    STATUS_ACTIVE = 'ACTIVE'
    STATUS_PENDING = 'PENDING'
    STATUS_CLOSED= 'CLOSED'

    STATUS_NOMES = {
        STATUS_ACTIVE: 'Ativo',
        STATUS_PENDING: 'Pendente',
        STATUS_CLOSED: 'Encerrado'
    }

    STATUS_CHOICES = (
        (STATUS_ACTIVE, STATUS_NOMES[STATUS_ACTIVE]),
        (STATUS_PENDING, STATUS_NOMES[STATUS_PENDING]),
        (STATUS_CLOSED, STATUS_NOMES[STATUS_CLOSED]),
    )

    title = models.CharField('Título do Produto', max_length=255)
    slug = models.SlugField(max_length=255, null=False, blank=True, unique=True)
    description = RichTextField(blank=True,null=False)
    old_price = models.DecimalField('Preço Antigo',max_digits=8, decimal_places=2,blank=True,null=True)
    price = models.DecimalField('Preço do Produto',max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='img/products/',blank=True,null=True,max_length=255)
    image_social = models.ImageField(upload_to='img/products/social/',blank=True,null=True,max_length=255)

    likes = models.ManyToManyField(User, related_name='product_likes', blank=True)
    status = models.CharField('status',max_length=20,choices=STATUS_CHOICES, default=STATUS_PENDING)
    
    store = models.ForeignKey(Store,on_delete=models.CASCADE,related_name="product_store")
    user = models.ForeignKey(User, on_delete= models.CASCADE ,related_name="user_posts")
    long_url = models.URLField(max_length=400)
    short_url = models.CharField(max_length=100, blank=True,null=True)
    coupon = models.CharField("Cupom",max_length=40, blank=True)
  
    subcategory = models.ForeignKey(SubCategory, on_delete= models.SET_NULL, blank=False,null=True)
    freight = models.ForeignKey(Freight, on_delete= models.SET_NULL, blank=False,null=True)
    warning =  models.ForeignKey(Warning, on_delete= models.CASCADE, blank=True,null=True)
    form_payment = models.ForeignKey(Form_Payment, on_delete= models.SET_NULL, blank=False,null=True)

    relevant = models.BooleanField(default=False)
    exclusive = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    whatsapp = models.BooleanField(default=False)
    telegram = models.BooleanField(default=False)
    instagram = models.BooleanField(default=False)
    facebook = models.BooleanField(default=False)
    class Meta:
        verbose_name="Produto" 

    def __str__(self):
        return '{}'.format(self.title)

    @property
    def number_of_likes(self):
        return self.likes.count()
    
    def save(self, *args, **kwargs):    
       
        if self.slug == '' or self.slug == None:
            self.slug = unique_slug_generator(self)

        super().save()

        if self.image_social:
            self.resize_image(self.image_social)

   
        # print(self.slug,'aaa\n\n')
 

    #resize image social
    def resize_image(self, image):
        image_s = Image.open(self.image_social) # Open image using self
     
        if image_s.height > 400 or image_s.width > 300:
            new_img = (400, 300)
            image_s.thumbnail(new_img)
            image_s.save(self.image_social.path,"JPEG",quality=80)


def update_cache_product(sender, instance, created, *args, **kwargs):
    cache.clear()

post_save.connect(update_cache_product, sender=Product)


class Comment(models.Model):  
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    active = models.BooleanField(default=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    author  = models.ForeignKey('authentication.User',on_delete = models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True,on_delete=models.CASCADE, related_name='replies')
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    
    @property
    def number_of_likes(self):
        return self.likes.count() 

    class Meta:
        ordering=('created',)
        verbose_name="Comentário" 
    def __str__(self):
       return 'Criado  por {}'.format(self.author.username)
   
class Report_Problem(models.Model):
    TYPE_CHOICES = (
        ('a','Esta Oferta Terminou'),
        ('b','Produto Caro'),
        ('c','Cupom Encerrado'),
        ('d','Oferta Já Foi Postada'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_report_problem_post')
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    checked = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Produtos Reportado'
    