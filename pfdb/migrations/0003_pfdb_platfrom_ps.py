# Generated by Django 2.0 on 2018-07-19 08:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pfdb', '0002_auto_20180509_1405'),
    ]

    operations = [
        migrations.AddField(
            model_name='pfdb',
            name='platfrom_ps',
            field=models.CharField(default=django.utils.timezone.now, max_length=128, verbose_name='备注'),
            preserve_default=False,
        ),
    ]
