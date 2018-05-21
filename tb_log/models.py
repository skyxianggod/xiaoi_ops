from django.db import models

# Create your models here.
from assets.models import assets
class tb_log(models.Model):

    uid = models.ForeignKey(to=assets,to_field='uid',on_delete=models.CASCADE)
