from django.shortcuts import render,HttpResponse,HttpResponseRedirect
import time
from django.urls import reverse_lazy
# from assets.urls import *
# Create your views here.
from django.views.generic import  ListView
from tb_log import models
from xiaoi_ops import  settings
from django.db.models import Q

class LogView(ListView):
    template_name = 'assets/tb_log.html'
    model = models.tb_log
    context_object_name = 'log_list'
    paginate_by = settings.DISPLAY_PER_PAGE
    ordering = ("id")
    def get_queryset(self):
        if self.request.GET.get('name'):
            query = self.request.GET.get('name', None)
            # print(query)
            queryset =super().get_queryset().filter(Q(uid_id=query)).order_by('id')
        else:
            queryset = super().get_queryset()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):

        search_data = self.request.GET.copy()
        print(search_data)
        try:
            search_data.pop("page")

        except BaseException as e:
            pass
        print(search_data.dict())
        print(search_data.urlencode())
        # context.update(search_data.dict())
        # 左侧导航站展开  "asset_active": "active",
        context = {
            "search_data": search_data.urlencode(),
            "assets_class": 'active',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


def logcreate(request,**kwargs):
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

