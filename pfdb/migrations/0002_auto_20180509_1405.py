# Generated by Django 2.0 on 2018-05-09 14:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('pfdb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
                model_name='pfdb',
                name='platfrom_name',
                field=models.CharField(max_length=64, verbose_name='平台名称'),
        ),
        migrations.AlterField(
                model_name='pfdb',
                name='platfrom_url',
                field=models.URLField(max_length=128, verbose_name='平台地址'),
        ),
    ]
