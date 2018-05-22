from django.shortcuts import render,HttpResponse,HttpResponseRedirect
import time
from django.urls import reverse_lazy
# from assets.urls import *
# Create your views here.
from tb_log import models
def tb_log(request,**kwargs):
    if request.method == "GET":
        a=request.path
        user = a.split('.')[0].split('-')[-1]
        pk = a.split('.')[0].split('-')[-2]
        kw = a.split('.')[0].split('-')[1]
        print(pk,kw)
    if kw == 'c':
        str1=str(pk)+'在'+time.strftime("%Y-%m-%d",time.localtime(time.time()))+'被录入'
        # print(str1)
    if kw == 'l':
        str1=str(pk)+'在'+time.strftime("%Y-%m-%d",time.localtime(time.time()))+'被'+user+'领用'

    if kw == 'o':
        str1=str(pk)+'在'+time.strftime("%Y-%m-%d",time.localtime(time.time()))+'被'+user+'借用'

    if kw == 'i':
        str1=str(pk)+'在'+time.strftime("%Y-%m-%d",time.localtime(time.time()))+'归还成功'

    try:
        models.tb_log.objects.create(uid_id=pk,log_info=str1)
    except BaseException :
            return HttpResponse('数据录入成功，操作日志录入失败，请联系开发人员')
    else:
        return HttpResponseRedirect(reverse_lazy('assets:assets_list'))

