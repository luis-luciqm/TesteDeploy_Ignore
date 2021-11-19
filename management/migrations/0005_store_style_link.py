# Generated by Django 3.2.6 on 2021-10-08 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0004_store_id_partner'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='style_link',
            field=models.CharField(choices=[('I', 'Início'), ('M', 'Meio'), ('F', 'Fim')], default='I', max_length=100, verbose_name='style_link'),
        ),
    ]
