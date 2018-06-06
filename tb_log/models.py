from django.db import models

# Create your models here.
from assets.models import assets

class tb_log(models.Model):

    uid = models.ForeignKey(to=assets,to_field='uid',on_delete=models.CASCADE,verbose_name='资产编号')
    log_info = models.TextField(verbose_name='操作记录')
    user = models.CharField(verbose_name='操作人', max_length=24)
