# Generated by Django 3.2.6 on 2021-10-18 11:41

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0025_auto_20211018_0830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='product_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
