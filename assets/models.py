from django.db import models

# Create your models here.

class assets(models.Model):

    uid = models.IntegerField(primary_key=True,verbose_name='资产编号',db_index=True)
    utype = models.CharField(max_length=64,verbose_name='设备类型')
    usize = models.CharField(max_length=64,verbose_name='设备型号')
    uconf = models.TextField(max_length=128,verbose_name='设备配置')
    active = models.ForeignKey(default=1,to=active,to_field=id,on_delete=models.CASCADE,verbose_name='状态')
    ctime = models.DateField(verbose_name='入库时间')

class active(models.Model):
    name = models.CharField(max_length=24,verbose_name='状态')

