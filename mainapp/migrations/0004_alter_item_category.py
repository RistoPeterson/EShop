# Generated by Django 4.2.1 on 2023-05-31 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_alter_item_discount_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('G', 'Garden'), ('V', 'Varia'), ('H', 'Home'), ('C', 'Car'), ('18', '18+')], max_length=5),
        ),
    ]
