# Generated by Django 5.0 on 2024-01-24 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_reservation_menu_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='reservation_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]