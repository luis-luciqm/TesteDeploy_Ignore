# Generated by Django 3.2.6 on 2021-10-14 19:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0023_alter_comment_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='likes',
            field=models.ManyToManyField(related_name='product_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
