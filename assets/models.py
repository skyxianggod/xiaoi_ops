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

    uid = models.CharField(max_length=24,primary_key=True,verbose_name='资产编号',db_index=True)
    utype = models.ForeignKey(to=platform,on_delete=models.CASCADE,to_field='id',verbose_name='设备类型')
    usize = models.ForeignKey(to=platform_size,on_delete=models.CASCADE,to_field='id',verbose_name='设备型号')
    uconf = models.TextField(max_length=128,verbose_name='设备配置')
    active = models.ForeignKey(to=active,to_field='id',on_delete=models.CASCADE,verbose_name='状态',default=1)
    ctime = models.DateField(verbose_name='入库时间')
    user = models.CharField(verbose_name='使用人',max_length=24,db_index=True,null=True,blank=True)
    otime = models.DateField(verbose_name='领（借）用时间',null=True,blank=True)
    gtime = models.DateField(verbose_name='归还时间',null=True,blank=True)
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
