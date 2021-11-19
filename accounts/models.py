from django.db import models

# Create your models here.

class TesteApp(models.Model):
    nome = models.CharField(max_length=250)
    cpf = models.CharField(max_length=25)