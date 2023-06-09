# Generated by Django 4.2 on 2023-07-14 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_rename_flat_number_billingaddress_apartment_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PopularItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('popularity_count', models.IntegerField(default=0)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.item')),
            ],
        ),
    ]
