# Generated by Django 3.2.6 on 2021-09-22 01:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_auto_20210921_2220'),
        ('product', '0003_auto_20210921_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='management.subcategory'),
        ),
    ]
