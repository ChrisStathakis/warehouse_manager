# Generated by Django 3.0.1 on 2021-02-16 05:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('costumers', '0041_auto_20210216_0734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='costumer',
            name='cellphone',
            field=models.CharField(blank=True, max_length=200, verbose_name='Κινητό'),
        ),
        migrations.AlterField(
            model_name='costumer',
            name='phone',
            field=models.CharField(blank=True, max_length=200, verbose_name='Τηλέφωνο'),
        ),
        migrations.AlterField(
            model_name='paymentinvoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 16, 5, 34, 34, 703364, tzinfo=utc), verbose_name='Ημερομηνία'),
        ),
    ]