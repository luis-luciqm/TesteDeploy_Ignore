# Generated by Django 3.2.6 on 2021-10-12 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='report_problem',
            name='checked',
            field=models.BooleanField(default=False),
        ),
    ]
