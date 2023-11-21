# Generated by Django 2.2.4 on 2019-09-17 14:59

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0010_auto_20190917_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='site',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='cellphone',
            field=models.CharField(blank=True, max_length=200, verbose_name='Κινητό'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='phone',
            field=models.CharField(blank=True, max_length=200, verbose_name='Σταθερο Τηλεφωνο'),
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('text', tinymce.models.HTMLField(blank=True)),
                ('vendor_related', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='vendors.Vendor')),
            ],
        ),
    ]
