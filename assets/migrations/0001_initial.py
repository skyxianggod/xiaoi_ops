# Generated by Django 2.0 on 2018-05-23 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('base_info', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
                name='active',
                fields=[
                    ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                    ('name', models.CharField(max_length=24, unique=True, verbose_name='状态')),
                ],
                options={
                    'verbose_name': '资产状态',
                    'verbose_name_plural': '资产状态',
                    'db_table': 'active',
                },
        ),
        migrations.CreateModel(
                name='assets',
                fields=[
                    ('uid', models.CharField(db_index=True, max_length=24, primary_key=True, serialize=False,
                                             verbose_name='资产编号')),
                    ('uconf', models.TextField(max_length=128, verbose_name='设备配置')),
                    ('ctime', models.DateField(verbose_name='入库时间')),
                    ('user', models.CharField(blank=True, db_index=True, max_length=24, null=True, verbose_name='使用人')),
                    ('otime', models.DateField(blank=True, null=True, verbose_name='领（借）用时间')),
                    ('gtime', models.DateField(blank=True, null=True, verbose_name='归还时间')),
                    ('active',
                     models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='assets.active',
                                       verbose_name='状态')),
                    ('usize',
                     models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_info.platform_size',
                                       verbose_name='设备型号')),
                    ('utype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_info.platform',
                                                verbose_name='设备类型')),
                ],
                options={
                    'verbose_name': '固定资产',
                    'verbose_name_plural': '固定资产',
                    'db_table': 'assets',
                    'permissions': {('read_assets', 'quit只读资产库')},
                },
        ),
    ]
