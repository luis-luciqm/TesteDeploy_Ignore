# Generated by Django 3.2.6 on 2021-11-17 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groupswhats', '0003_auto_20211117_1137'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]