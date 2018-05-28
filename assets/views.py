from django.shortcuts import render,get_object_or_404,HttpResponseRedirect
import time,json
import re
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View,DetailView
from xiaoi_ops import settings
from  .models import *
from .form import AssetsForm,AssetsForm_give,AssetsForm_in
from django.core import serializers
from django.db.models import Q
from tb_log.models import tb_log

class AssetsList(LoginRequiredMixin,ListView):
    template_name = 'assets/assets.html'
    model = assets
    context_object_name = 'assets_list'
    paginate_by = settings.DISPLAY_PER_PAGE
    ordering = ("active_id")


    def get_context_data(self, *, object_list=None, **kwargs):

        search_data = self.request.GET.copy()
        print(search_data)
        try:
            search_data.pop("page")

        except BaseException as e:
            pass
        # print(search_data.dict())
        # print(search_data.urlencode())
        # context.update(search_data.dict())
        # 左侧导航站展开  "asset_active": "active",
        context = {
            "search_data": search_data.urlencode(),
            "assets_class": 'active',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)



    def get_queryset(self):
        if self.request.GET.get('name'):
            query = self.request.GET.get('name', None)
            print(query)
            try:
                queryset =super().get_queryset().filter(Q(user=query)|Q(uid=query)|Q(active_id=query)).order_by('active_id')
            except BaseException:
                queryset =super().get_queryset().filter(Q(user=query)).order_by('active_id')
        else:
            queryset = super().get_queryset()
        return queryset




class AssetsAdd(LoginRequiredMixin, CreateView):
    """增加"""
    model = assets
    form_class = AssetsForm
    template_name = 'assets/assets-add-update.html'
    # success_url = reverse_lazy('assets:assets_list')

    def post(self, request, *args, **kwargs):
        print(self.request.POST)
        pk=request.POST['uid']
        print(pk)
        self.success_url=reverse_lazy('tb_log:tb_log_create',kwargs={'pk':pk,'kw':'c','user':'c'})
        return super().post(request, *args, **kwargs)

class AssetsUpdateDtail(LoginRequiredMixin, UpdateView):
    model = assets
    form_class = AssetsForm
    template_name = 'assets/assets-update.html'
    context_object_name = 'obj'
    # success_url = reverse_lazy('assets:assets_list')
    def post(self, request, *args, **kwargs):
        print(self.request.POST)
        pk=request.POST['uid']
        print(pk)
        self.success_url=reverse_lazy('tb_log:tb_log_create',kwargs={'pk':pk,'kw':'u','user':'c'})
        return super().post(request, *args, **kwargs)

def getdata(request):
    pk = request.GET['pk']
    plat = get_object_or_404(platform, pk=pk)
    size = plat.platform_size_set.all()
    data = serializers.serialize('json', size)
    print(data)
    return HttpResponse(data, content_type='application/json')


class AssetsDetail(LoginRequiredMixin,DetailView):
    model = assets
    template_name = 'assets/assets-detail.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg,None)
        detail = assets.objects.get(uid=pk)
        text = {
            "detail":detail,
            "nid":pk,
        }
        kwargs.update(text)
        return super().get_context_data(**kwargs)



class AssetsUpdate(LoginRequiredMixin,UpdateView):
    '''借用和领用资产'''
    model = assets
    form_class = AssetsForm_give
    template_name = 'assets/assets-add-update-give.html'
    # success_url = reverse_lazy('assets:assets_list')

    def post(self, request, *args, **kwargs):

        pk = self.request.path.split('.')[0].split('-')[-1]
        # print(pk)

        # print(reverse_lazy('tb_log:tb_log_create',kwargs={'pk':pk,}))

        # print(self.request.path)
        b=self.request.path
        a=self.request.POST.copy()
        ret=re.search('-g-',b)

        user = self.request.POST['user']
        if assets.objects.get(uid=pk).active_id==1:
            if ret is None:
                a['active'] = 3
                self.success_url=reverse_lazy('tb_log:tb_log_create',kwargs={'pk':pk,'kw':'o','user':user})
            else:
                a['active'] = 2
                self.success_url=reverse_lazy('tb_log:tb_log_create',kwargs={'pk':pk,'kw':'l','user':user})
            # print(a)
            self.request.POST = a
        else :
            return HttpResponse('请先归还资产')

        return super().post(request, *args, **kwargs)


class AssetsUpdatein(LoginRequiredMixin,UpdateView):
    '''归还资产和资产报废'''
    model = assets
    form_class = AssetsForm_in
    template_name = 'assets/assets-add-update-in.html'
    # success_url = reverse_lazy('assets:assets_list')

    def post(self, request, *args, **kwargs):
        b=self.request.path
        pk = self.request.path.split('.')[0].split('-')[-1]
        a=self.request.POST.copy()
        ret=re.search('-i-',b)
        if ret :
            a['active']=1
            a['user']=''
            a['otime']=''
            self.success_url=reverse_lazy('tb_log:tb_log_create',kwargs={'pk':pk,'kw':'i','user':'c'})

        else:
            a['active']=5
            a['user']=''
            a['otime']=''
            self.success_url=reverse_lazy('tb_log:tb_log_create',kwargs={'pk':pk,'kw':'p','user':'c'})


        self.request.POST=a
        return super().post(request, *args, **kwargs)



def repair(request,**kwargs):
    '''维修资产'''
    if request.method == 'GET':
        return render(request,'assets/wx_log.html')

    if request.method == 'POST':

        pk = request.path.split('.')[0].split('-')[-1]
        str_id = request.POST['wx']

        if assets.objects.get(uid=pk).active_id==1:

            assets.objects.filter(uid=pk).update(active_id=4)

        else :
            return HttpResponse('请先归还资产')
        str1=str(pk)+'在'+time.strftime("%Y-%m-%d",time.localtime(time.time()))+'报修'+'  报修原因：'+str_id
        try:
            tb_log.objects.create(uid_id=pk,log_info=str1)
        except BaseException :
                return HttpResponse('数据录入成功，操作日志录入失败，请联系开发人员')
        else:
            return HttpResponseRedirect(reverse_lazy('assets:assets_list'))


def AssetsZtree(request):
    """
    获取 区域 资产树 的相关数据
    :param request:
    :return:
    """

    manager = active.objects.values()
    data = [{"id": "1111", "pId": "0", "name": "状态"}, ]
    for i in manager:
        # print(i['id'])
        data.append({"id": i['id'], "pId": "1111", "name": i['name'], "page": "xx.action"}, )
    return HttpResponse(json.dumps(data), content_type='application/json')






    #

    # a=self.request.POST.copy()
    # a['active']=1
    # a['user']=''
    # a['otime']=''
    # print(a)
    # self.success_url=reverse_lazy('tb_log:tb_log_create',kwargs={'pk':pk,'kw':'i','user':'c'})
    # self.request.POST=a





