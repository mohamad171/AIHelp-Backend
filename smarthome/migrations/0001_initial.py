# Generated by Django 2.1.1 on 2019-04-07 07:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bulb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BulbName', models.TextField(verbose_name='نام لامپ')),
                ('BublStatus', models.BooleanField(verbose_name='وضعیت لامپ')),
                ('LastModify', models.DateTimeField(default=django.utils.timezone.now, verbose_name='آخرین تغییر')),
            ],
            options={
                'verbose_name': 'لامپ',
                'verbose_name_plural': 'لامپ ها',
            },
        ),
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('HomeName', models.TextField(verbose_name='نام خانه')),
                ('HomeAddress', models.TextField(verbose_name='آدرس خانه')),
            ],
            options={
                'verbose_name': 'خانه',
                'verbose_name_plural': 'خانه ها',
            },
        ),
        migrations.AddField(
            model_name='bulb',
            name='Home',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smarthome.Home'),
        ),
    ]
