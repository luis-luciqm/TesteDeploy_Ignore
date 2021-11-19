# Generated by Django 3.2.6 on 2021-09-21 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
        ('product', '0002_remove_product_subcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='management.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='img/products/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='short_url',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AlterField(
            model_name='product',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_store', to='management.store'),
        ),
    ]
