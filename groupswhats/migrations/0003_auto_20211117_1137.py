# Generated by Django 3.2.6 on 2021-11-17 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groupswhats', '0002_auto_20211117_1117'),
    ]

    operations = [
        migrations.RenameField(
            model_name='margin',
            old_name='num1',
            new_name='finish',
        ),
        migrations.RenameField(
            model_name='margin',
            old_name='num2',
            new_name='init',
        ),
    ]