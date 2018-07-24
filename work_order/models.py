# Create your models here.
from django.db import models

class order(models.Model):

    STAUTS_CHOICES=(
        ("待处理",'待处理'),
        ('已完成','已完成'),
    )

    event_name = models.CharField(max_length=64,verbose_name='事件名称')
    event_ps = models.CharField(max_length=128,verbose_name='事件描述')
    person = models.CharField(max_length=14,verbose_name='处理人')
    event_starttime = models.DateField(verbose_name='事件创建时间',auto_now=True)
    event_endtime = models.DateField(verbose_name='计划完成时间')
    event_progress = models.CharField(verbose_name='进度',max_length=24)
    event_status = models.CharField(verbose_name='时间状态',choices=STAUTS_CHOICES,max_length=24)


    class  Meta:
        db_table ="order"
        verbose_name="工作日志"
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.id