# Generated by Django 2.2 on 2019-04-26 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0014_auto_20190426_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='choicesAccepted',
            field=models.IntegerField(default=1),
        ),
    ]
