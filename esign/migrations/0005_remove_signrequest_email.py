# Generated by Django 3.1.4 on 2021-02-01 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('esign', '0004_auto_20210201_1903'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signrequest',
            name='email',
        ),
    ]
