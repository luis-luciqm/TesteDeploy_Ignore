# models.py
from django.conf import settings
from django.db import models


class Book(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    co_authors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='co_authored_by')

class Country(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey('Country', related_name="cities",on_delete=models.CASCADE)

    def __str__(self):
        return self.name