# Generated by Django 3.2.6 on 2021-10-30 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0036_auto_20211029_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Ativo'), ('INACTIVE', 'Inativo'), ('PENDING', 'Pendente'), ('CLOSED', 'Encerrado')], default='PENDING', max_length=20, verbose_name='status'),
        ),
    ]