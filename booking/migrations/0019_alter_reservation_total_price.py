# Generated by Django 3.2.19 on 2023-05-21 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0018_alter_gametable_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]