# Generated by Django 4.2 on 2023-06-14 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_billingaddress_country'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billingaddress',
            old_name='flat_number',
            new_name='apartment',
        ),
        migrations.RenameField(
            model_name='billingaddress',
            old_name='street_name',
            new_name='street_address',
        ),
    ]
