# Generated by Django 3.2.6 on 2021-10-23 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0031_product_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image_url',
        ),
    ]
