# Generated by Django 3.2.19 on 2023-05-29 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gametable',
            options={'ordering': ['table_number']},
        ),
    ]
