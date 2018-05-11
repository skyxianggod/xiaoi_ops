# Generated by Django 2.0 on 2018-05-11 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='department',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='部门编号')),
                ('name', models.CharField(max_length=16, verbose_name='部门名称')),
            ],
            options={
                'verbose_name': '部门信息',
                'verbose_name_plural': '部门信息',
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='person',
            fields=[
                ('id', models.CharField(max_length=24, primary_key=True, serialize=False, verbose_name='工号')),
                ('name', models.CharField(max_length=24, verbose_name='姓名')),
                ('mobile', models.CharField(max_length=11, verbose_name='手机号码')),
                ('part', models.ForeignKey(max_length=24, on_delete=django.db.models.deletion.CASCADE, to='base_info.department', verbose_name='部门')),
            ],
            options={
                'verbose_name': '员工信息',
                'verbose_name_plural': '员工信息',
                'db_table': 'person_info',
            },
        ),
        migrations.CreateModel(
            name='platform',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='id')),
                ('name', models.CharField(max_length=24, verbose_name='设备类型')),
            ],
            options={
                'verbose_name': '设备类型',
                'verbose_name_plural': '设备类型',
                'db_table': 'platform',
            },
        ),
        migrations.CreateModel(
            name='platform_size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24, verbose_name='设备型号')),
                ('platform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_info.platform', verbose_name='设备型号')),
            ],
            options={
                'verbose_name': '设备型号',
                'verbose_name_plural': '设备型号',
                'db_table': 'platform_size',
            },
        ),
        migrations.CreateModel(
            name='shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24, verbose_name='商家名称')),
                ('user', models.CharField(max_length=24, verbose_name='联系人')),
                ('mobile', models.CharField(max_length=11, verbose_name='手机号码')),
                ('addr', models.CharField(blank=True, max_length=24, verbose_name='商家地址')),
            ],
            options={
                'verbose_name': '商家信息',
                'verbose_name_plural': '商家信息',
                'db_table': 'shop',
            },
        ),
    ]
