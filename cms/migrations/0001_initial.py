# Generated by Django 3.1.6 on 2021-02-16 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questname', models.CharField(max_length=255, verbose_name='クエスト名')),
                ('rank', models.CharField(max_length=255, verbose_name='ランク')),
                ('target', models.CharField(max_length=255, verbose_name='ターゲット')),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('runner', models.CharField(max_length=255, verbose_name='Player Name')),
                ('party', models.CharField(choices=[('S', '1'), ('P', '2'), ('M', '3or4')], max_length=255, verbose_name='Party')),
                ('cleartime', models.DurationField()),
                ('weapon', models.CharField(max_length=255, verbose_name='Weapon')),
                ('rules', models.CharField(choices=[('FR', 'FreeStyle'), ('TW', 'TA-wiki-rules'), ('PD', 'Production-Equipment')], max_length=255, verbose_name='Rules')),
                ('platform', models.CharField(choices=[('SW', 'Switch'), ('PC', 'PC')], max_length=255, verbose_name='PlatForms')),
                ('problems', models.IntegerField(blank=True, default=0, verbose_name='Problem report')),
                ('quest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='cms.quest', verbose_name='Quest')),
            ],
        ),
    ]
