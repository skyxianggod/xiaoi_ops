# Generated by Django 2.0 on 2018-07-25 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_order', '0002_auto_20180725_1440'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='event_updatetime',
            field=models.DateField(auto_now=True, verbose_name='事件创建时间'),
        ),
    ]
