# Generated by Django 3.0.1 on 2021-01-09 11:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('costumers', '0027_auto_20201204_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentinvoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 9, 11, 22, 26, 645232, tzinfo=utc), verbose_name='Ημερομηνία'),
        ),
    ]