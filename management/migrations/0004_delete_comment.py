# Generated by Django 3.2.6 on 2021-10-08 00:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_alter_comment_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
