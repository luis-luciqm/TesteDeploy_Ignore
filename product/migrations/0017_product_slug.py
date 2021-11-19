# Generated by Django 3.2.6 on 2021-10-13 16:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0016_alter_report_problem_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default=uuid.uuid1, max_length=255, null=True),
        ),
    ]