from django.db import models
from django.utils.text import slugify

class GroupWhatsapp(models.Model):
    TYPE_SOCIAL = (
        ('W', 'WhatsApp'),
        ('I', 'Instagram'),
        ('T', 'Telegram')
    )

    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(name='name', max_length=200)
    link_invitation = models.CharField(name='link_convite', max_length=200)
    is_active = models.BooleanField(default=False, name='is_active')
    type_social = models.CharField(name='type_social', choices=TYPE_SOCIAL, max_length=20)
    
    class Meta:
        verbose_name = 'Grupos WhatsApp'

class Margin(models.Model):
    name = models.CharField(max_length=100)
    init = models.IntegerField()
    finish = models.IntegerField()
    slug = models.SlugField()
    
    class Meta:
        verbose_name = "Margen"
        
        
    def save(self, *args, **kwargs):
        if self.slug == '' or self.slug == None:
            self.slug = slugify(self.name)

        super().save()
        
class Message(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Mensagen"