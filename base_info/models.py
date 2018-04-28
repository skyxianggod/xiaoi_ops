from django.db import models


# Create your models here.
class person(models.Model):
    id = models.CharField(max_length=24, primary_key=True, blank=False, verbose_name='工号')
    name = models.CharField(max_length=24, blank=False, verbose_name='姓名')
    part = models.CharField(max_length=24, verbose_name='部门')
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
