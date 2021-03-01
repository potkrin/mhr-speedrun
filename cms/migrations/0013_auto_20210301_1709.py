# Generated by Django 3.1.6 on 2021-03-01 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_quest_recordnum'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weapon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Weapon Name')),
                ('imagepath', models.CharField(max_length=511, verbose_name='Image Path')),
            ],
        ),
        migrations.AlterField(
            model_name='record',
            name='weapon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cms.weapon', verbose_name='Weapon'),
        ),
    ]
