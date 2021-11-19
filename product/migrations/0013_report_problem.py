# Generated by Django 3.2.6 on 2021-10-11 18:08

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0012_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report_Problem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('type', models.CharField(choices=[('a', 'Esta Oferta Terminou'), ('b', 'Produto Caro'), ('c', 'Cupom Encerrado'), ('d', 'Oferta Já Foi Postada')], max_length=100)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_report_problem_post', to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='report_user_posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]