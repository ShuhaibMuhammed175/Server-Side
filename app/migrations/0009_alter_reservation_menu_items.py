# Generated by Django 5.0 on 2024-01-18 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_remove_reservation_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='menu_items',
            field=models.ManyToManyField(blank=True, null=True, to='app.menuitems'),
        ),
    ]
