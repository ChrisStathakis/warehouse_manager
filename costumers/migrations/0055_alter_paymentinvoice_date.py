# Generated by Django 3.2.7 on 2023-06-13 02:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('costumers', '0054_alter_paymentinvoice_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentinvoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 13, 2, 22, 0, 843242, tzinfo=utc), verbose_name='Ημερομηνία'),
        ),
    ]
