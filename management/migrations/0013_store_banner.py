# Generated by Django 3.2.6 on 2021-10-25 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0012_store_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='banner',
            field=models.FileField(blank=True, null=True, upload_to='img/loja/banner'),
        ),
    ]
