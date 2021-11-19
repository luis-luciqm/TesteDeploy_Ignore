# Generated by Django 3.2.6 on 2021-10-03 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_alter_product_warning'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image_social',
            field=models.ImageField(blank=True, null=True, upload_to='img/products/social/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='short_url',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
