# Generated by Django 3.2.6 on 2021-11-02 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0037_alter_product_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='exclusive',
            field=models.BooleanField(default=False),
        ),
    ]