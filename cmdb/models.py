

# Create your models here.
from django.db import models

class cmdb(models.Model):
    PLATFORM_CHOICES=(
        ("虚拟机","虚拟机"),
        ("物理机", "物理机"),
        ("其他", "其他"),
    )
    REGION_CHOICES=(
        ("香港",'香港'),
        ("上海",'上海'),
    )
    POWER_CHOICES=(
        ("是",'是'),
        ('否','否'),
    )

    MANAGER_CHOICES=(
        ('admin','admin'),
        ('其他','其他'),
    )
    PROJECT_CHOICES=(
        ('项目1','项目1'),
        ('项目2', '项目2'),
        ('项目3', '项目3'),
        ('其他', '其他')
    )

    id = models.AutoField(primary_key=True,verbose_name="id")
    UID = models.CharField(max_length=128, verbose_name='资产编号',null=True,blank=True)
    PID = models.CharField(max_length=128, verbose_name='序列号',null=True,blank=True)

    hostname = models.CharField(max_length=64, verbose_name='主机名',unique=True)
    network_ip = models.GenericIPAddressField(verbose_name='外网IP', null=True,blank=True)
    inner_ip = models.GenericIPAddressField(verbose_name='内网IP', null=True, blank=True)


    system = models.CharField(max_length=128,verbose_name='系统版本',null=True,blank=True)
    cpu = models.CharField(max_length=64,verbose_name='CPU',null=True,blank=True)
    memory = models.CharField(max_length=64, verbose_name='内存', null=True,blank=True)
    disk = models.CharField(max_length=256,verbose_name="硬盘",null=True,blank=True)
    netinfo = models.CharField(max_length=256,verbose_name="网卡",null=True,blank=True)


    platform =  models.CharField(max_length=128, choices=PLATFORM_CHOICES, verbose_name='机器类型')
    platform_size =  models.CharField(max_length=128, verbose_name='机器型号',null=True,blank=True)
    region =  models.CharField(max_length=128, choices=REGION_CHOICES, verbose_name='机柜名')
    power = models.CharField(max_length=128, choices=POWER_CHOICES, verbose_name='电源冗余')




    manager = models.CharField(max_length=128, choices=MANAGER_CHOICES, verbose_name='负责人')
    use = models.CharField(max_length=128,null=True,blank=True, verbose_name='使用人')
    project = models.CharField(max_length=128, choices=PROJECT_CHOICES, verbose_name='项目')

    ps = models.CharField(max_length=1024,verbose_name="备注（用途）",null=True,blank=True)
    # port = models.IntegerField(verbose_name="登录端口",default='22',null=True, blank=True)
    logintype = models.CharField(max_length=1024,verbose_name="登录方式",null=True,blank=True)

    ctime= models.CharField(max_length=64,null=True,verbose_name='申请时间',blank=True)
    utime = models.CharField(max_length=64,null=True,verbose_name='到期时间',blank=True)

    gtime= models.CharField(max_length=64,null=True,verbose_name='上架时间',blank=True)
    otime = models.CharField(max_length=64,null=True,verbose_name='下架时间',blank=True)





    class  Meta:
        db_table ="cmdb"
        verbose_name="资产管理"
        verbose_name_plural = '资产管理'
        permissions = {
            ('read_cmdb',u"只读资产管理"),
        }


    def __str__(self):
        return self.hostname