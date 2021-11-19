# Generated by Django 3.2.6 on 2021-10-18 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0024_product_likes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report_problem',
            options={'verbose_name': 'Produtos Reportado'},
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('ATIVO', 'Ativo'), ('INATIVO', 'Inativo'), ('PENDENTE', 'Pendente'), ('EXPIRADO', 'Expirado')], default='PENDENTE', max_length=20, verbose_name='status'),
        ),
    ]
