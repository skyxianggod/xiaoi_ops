# Create your models here.


# Create your models here.
from django.db import models


class gzdb(models.Model):
    # PLATFORM_CHOICES=(
    #     ("虚拟机","虚拟机"),
    #     ("物理机", "物理机"),
    #     ("其他", "其他"),
    # )
    # REGION_CHOICES=(
    #     ("香港",'香港'),
    #     ("上海",'上海'),
    # )
    # POWER_CHOICES=(
    #     ("是",'是'),
    #     ('否','否'),
    # )
    #
    # MANAGER_CHOICES=(
    #     ('admin','admin'),
    #     ('其他','其他'),
    # )
    # PROJECT_CHOICES=(
    #     ('项目1','项目1'),
    #     ('项目2', '项目2'),
    #     ('项目3', '项目3'),
    #     ('其他', '其他')
    # )
    #
    type = models.CharField(max_length=28, null=False, verbose_name='设备类型', blank=False, unique=True)
    type_size = models.CharField(max_length=28, null=False, verbose_name='设备型号', blank=False)
    id = models.CharField(primary_key=True, max_length=28, null=False, verbose_name='资产编号', blank=True)
    uid = models.CharField(max_length=28, null=True, verbose_name='设备编号', blank=True)
    sn = models.CharField(max_length=28, null=True, verbose_name='序列号', blank=True)
    stat = models.CharField(max_length=28, null=True, verbose_name='状态', blank=True)
    depart = models.CharField(max_length=28, null=True, verbose_name='部门', blank=True)
    addr = models.CharField(max_length=28, null=True, verbose_name='设备地址', blank=True)
    user = models.CharField(max_length=28, null=True, verbose_name='使用人', blank=True)
    ps = models.CharField(max_length=1024, verbose_name="备注（配置和用途）", null=True, blank=True)
    history = models.CharField(max_length=1024, verbose_name="历史记录", null=True, blank=True)

    class Meta:
        db_table = "gzdb"
        verbose_name = "固定资产管理"
        verbose_name_plural = '固定资产管理'
        permissions = {
            ('read_gzdb', u"只读资产管理"),
        }

    def __str__(self):
        return self.id
