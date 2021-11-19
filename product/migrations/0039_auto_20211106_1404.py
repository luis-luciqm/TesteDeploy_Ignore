# Generated by Django 3.2.6 on 2021-11-06 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0038_product_exclusive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='img/products/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image_social',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='img/products/social/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Ativo'), ('PENDING', 'Pendente'), ('CLOSED', 'Encerrado')], default='PENDING', max_length=20, verbose_name='status'),
        ),
    ]
