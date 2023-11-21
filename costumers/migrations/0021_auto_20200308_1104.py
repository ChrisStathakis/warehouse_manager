# Generated by Django 3.0.1 on 2020-03-08 09:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('costumers', '0020_auto_20200308_1017'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paymentinvoice',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='paymentinvoice',
            name='card_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='costumers.MyCard', verbose_name='Στάμπα'),
        ),
        migrations.AlterField(
            model_name='paymentinvoice',
            name='order_type',
            field=models.CharField(choices=[('a', 'Τιμολογιο'), ('b', 'Δελτιο Παραγγελίας'), ('c', 'Προπαραγγελία')], default='a', max_length=1, verbose_name='Ειδος Παραστατικου'),
        ),
        migrations.AlterUniqueTogether(
            name='paymentinvoice',
            unique_together={('number', 'series', 'order_type')},
        ),
    ]
