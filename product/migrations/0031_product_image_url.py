# Generated by Django 3.2.6 on 2021-10-22 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0030_alter_product_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
