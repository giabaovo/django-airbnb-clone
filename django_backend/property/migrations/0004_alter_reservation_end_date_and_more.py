# Generated by Django 5.1 on 2024-09-11 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0003_reservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
