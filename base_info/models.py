from django.db import models


# Create your models here.
class person(models.Model):
    id = models.CharField(max_length=24, primary_key=True, blank=False, verbose_name='工号')
    name = models.CharField(max_length=24, blank=False, verbose_name='姓名')
    part = models.ForeignKey(to='department',to_field='id',on_delete=models.CASCADE,max_length=24, verbose_name='部门')
    mobile = models.CharField(max_length=11, verbose_name='手机号码')

    class Meta:
        db_table = "person_info"
        verbose_name = "员工信息"
        verbose_name_plural = '员工信息'


class department(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, verbose_name='部门编号')
    name = models.CharField(max_length=16, blank=False, verbose_name='部门名称')

    class Meta:
        db_table = "department"
        verbose_name = "部门信息"
        verbose_name_plural = '部门信息'

    def __str__(self):
        return self.name


class shop(models.Model):
    name = models.CharField(max_length=24, blank=False, verbose_name='商家名称')
    user = models.CharField(max_length=24, blank=False, verbose_name='联系人')
    mobile = models.CharField(max_length=11, verbose_name='手机号码')
    addr = models.CharField(max_length=24, blank=True, verbose_name='商家地址')

    class Meta:
        db_table = "shop"
        verbose_name = "商家信息"
        verbose_name_plural = '商家信息'


class platform(models.Model):
    id =models.AutoField(primary_key=True, blank=False, verbose_name='id')
    name = models.CharField(max_length=24, verbose_name='设备类型')
    class Meta:
        db_table = "platform"
        verbose_name = "设备类型"
        verbose_name_plural = '设备类型'

    def __str__(self):
        return self.name


class platform_size(models.Model):

    name = models.CharField(max_length=24,verbose_name='设备型号')
    platform = models.ForeignKey(verbose_name="设备型号",to=platform,to_field='id',on_delete=models.CASCADE)
    class Meta:
        db_table = "platform_size"
        verbose_name = "设备型号"
        verbose_name_plural = '设备型号'
    def __str__(self):
        return self.name



class platform_asstes(models.Model):

    name = models.CharField(max_length=24,verbose_name='设备配置')
    platform_size = models.ForeignKey(verbose_name="设备配置",to=platform_size,to_field='id',on_delete=models.CASCADE)
    class Meta:
        db_table = "platform_asstes"
        verbose_name = "设备配置"
        verbose_name_plural = '设备配置'


