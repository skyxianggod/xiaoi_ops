from django.db import models

from base_info.models import platform,platform_size


# Create your models here.
class active(models.Model):
    name = models.CharField(max_length=24,verbose_name='状态',unique=True)

    class Meta:
        db_table = 'active'
        verbose_name = '资产状态'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


class assets(models.Model):
    active = models.ForeignKey(to=active, to_field='id', on_delete=models.CASCADE, verbose_name='状态', default=1)
    uid = models.CharField(max_length=24,primary_key=True,verbose_name='资产编号',db_index=True)
    pid = models.CharField(verbose_name='设备号', max_length=24, null=True, blank=True)
    utype = models.ForeignKey(to=platform,on_delete=models.CASCADE,to_field='id',verbose_name='设备类型')
    usize = models.ForeignKey(to=platform_size,on_delete=models.CASCADE,to_field='id',verbose_name='设备型号')
    user = models.CharField(verbose_name='使用人',max_length=24,db_index=True,null=True,blank=True)
    upart = models.CharField(verbose_name='部门', max_length=24, db_index=True, null=True, blank=True)
    addr = models.CharField(verbose_name='存放地点', max_length=24, null=True, blank=True, default='库房')
    cpu = models.CharField(max_length=64, verbose_name='CPU', null=True, blank=True)
    mem = models.CharField(max_length=64, verbose_name='内存', null=True, blank=True)
    disk = models.CharField(max_length=256, verbose_name="硬盘", null=True, blank=True)
    sn = models.CharField(verbose_name='SN号', max_length=24, null=True, blank=True)
    nmac = models.CharField(verbose_name='有线mac', max_length=24, null=True, blank=True)
    wmac = models.CharField(verbose_name='无线mac', max_length=24, null=True, blank=True)
    ctime = models.DateField(verbose_name='入库时间')
    otime = models.DateField(verbose_name='领（借）用时间', null=True, blank=True)
    gtime = models.DateField(verbose_name='归还(报废)时间', null=True, blank=True)
    ps = models.CharField(verbose_name='备注', max_length=24, null=True, blank=True)





    class Meta:
        db_table = "assets"
        verbose_name = "固定资产"
        verbose_name_plural = '固定资产'
        permissions = {
            ('read_assets', u"quit"
                            u"只读资产库"),
        }

    def __str__(self):
        return str(self.uid)

# active.objects.create(name='在库')
# active.objects.create(name='领用')
# active.objects.create(name='借用')
# active.objects.create(name='维修')
# active.objects.create(name='报废')
#     # def __str__(self):
    #     return self.name
