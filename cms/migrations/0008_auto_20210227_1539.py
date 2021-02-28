# Generated by Django 3.1.6 on 2021-02-27 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_auto_20210227_1253'),
    ]

    operations = [
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monstername', models.CharField(max_length=255, verbose_name='Monster Name')),
                ('imagepath', models.CharField(max_length=511, verbose_name='Image Path')),
            ],
        ),
        migrations.DeleteModel(
            name='Monster',
        ),
        migrations.RemoveField(
            model_name='quest',
            name='imagepath',
        ),
        migrations.AlterField(
            model_name='quest',
            name='target',
            field=models.CharField(default='test', max_length=255, verbose_name='Target'),
        ),
    ]
