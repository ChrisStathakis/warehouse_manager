# Generated by Django 2.2.4 on 2019-09-10 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0005_auto_20190910_1206'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoice',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['-date']},
        ),
    ]