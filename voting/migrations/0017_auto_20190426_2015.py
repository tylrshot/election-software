# Generated by Django 2.2 on 2019-04-27 00:15

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0016_auto_20190426_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='response',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None), blank=True, null=True, size=None),
        ),
    ]
