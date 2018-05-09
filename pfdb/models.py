# Create your models here.
from django.db import models

class pfdb(models.Model):

    id = models.AutoField(primary_key=True,verbose_name="id")
    platfrom_name = models.CharField(max_length=64,verbose_name="平台名称")
    platfrom_url = models.URLField(max_length=128,verbose_name="平台地址")

    class Meta:
        db_table ="pfdb"
        verbose_name="平台管理"
        verbose_name_plural = '平台管理'

    def __str__(self):
        return self.platfrom_name



