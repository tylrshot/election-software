# Generated by Django 2.2 on 2019-04-21 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0003_auto_20190421_1553'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]