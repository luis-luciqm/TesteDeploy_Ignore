# Generated by Django 3.2.6 on 2021-10-02 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_product_old_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_social',
            field=models.ImageField(blank=True, null=True, upload_to='img/products/social'),
        ),
    ]
