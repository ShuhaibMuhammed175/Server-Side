# Generated by Django 5.0 on 2024-01-06 07:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone_number', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('description', models.TextField()),
                ('address', models.CharField(max_length=100)),
                ('opening_time', models.TimeField()),
                ('closing_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='restaurant_location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.TextField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='restaurant_image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='restaurant_images/')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.restaurant')),
            ],
        ),
        migrations.AddField(
            model_name='restaurant',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.restaurant_location'),
        ),
    ]
