# Generated by Django 3.1.4 on 2021-02-02 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('esign', '0006_auto_20210201_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipient',
            name='recipient_id',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
