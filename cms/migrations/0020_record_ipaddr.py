# Generated by Django 3.1.6 on 2021-03-07 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0019_auto_20210303_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='ipaddr',
            field=models.GenericIPAddressField(default='127.0.0.1', verbose_name='client-ipaddress'),
        ),
    ]
