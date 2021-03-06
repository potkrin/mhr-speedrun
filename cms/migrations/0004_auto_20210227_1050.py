# Generated by Django 3.1.6 on 2021-02-27 01:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20210220_1005'),
    ]

    operations = [
        migrations.CreateModel(
            name='Monster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monstername', models.CharField(max_length=255, verbose_name='Monster Name')),
                ('imagpath', models.CharField(max_length=1023, verbose_name='Image Path')),
            ],
        ),
        migrations.AlterField(
            model_name='record',
            name='link',
            field=models.URLField(max_length=2047, validators=[django.core.validators.RegexValidator(message='aaaaaaaaaaaa!!!', regex='^https://www.youtube.com/watch|https://www.nicovideo.jp/watch/|https://www.bilibili.com/video/')]),
        ),
        migrations.AlterField(
            model_name='record',
            name='weapon',
            field=models.CharField(choices=[('GS', 'great-sword'), ('LS', 'long-sword'), ('SNS', 'sword-and-shield'), ('DB', 'dual-blades'), ('HM', 'hammer'), ('HH', 'hunting-horn'), ('LN', 'lance'), ('GL', 'gunlance'), ('SA', 'switch-axe'), ('CB', 'charge-blade'), ('IG', 'insect-glaive'), ('LBG', 'light-bowgun'), ('HBG', 'heavy-bowgun'), ('BOW', 'bow'), ('MIX', 'mixed')], max_length=255, verbose_name='Weapon'),
        ),
        migrations.AddField(
            model_name='quest',
            name='monsters',
            field=models.ManyToManyField(to='cms.Monster'),
        ),
    ]
