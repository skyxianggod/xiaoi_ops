import time

from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy

# from assets.urls import *
# Create your views here.
from django.views.generic import  ListView
from tb_log import models
from xiaoi_ops import  settings
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


class LogView(LoginRequiredMixin, ListView):
    template_name = 'assets/tb_log.html'
    model = models.tb_log
    context_object_name = 'log_list'
    paginate_by = settings.DISPLAY_PER_PAGE
    ordering = ("-id")
    def get_queryset(self):

        if self.request.GET.get('name'):
            query = self.request.GET.get('name', None)
            # print(query)
            queryset =super().get_queryset().filter(Q(uid_id=query)).order_by('id')
        else:
            queryset = super().get_queryset()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):

        # 高级分页
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')

        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        # print(pagination_data)
        # print(is_paginated,paginator,page)
        ########
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
            # "pagination_data":pagination_data,
        }
        context.update(pagination_data)
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def pagination_data(self, paginator, page, is_paginated):

        if not is_paginated:
            return {}

        left = []
        right = []

        left_has_more = False
        right_has_more = False

        first = False
        last = False
        # 当前页码
        page_number = page.number
        # 总页数
        total_pages = paginator.num_pages
        # 页码列表
        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 3]

            if right[-1] < total_pages - 1:
                right_has_more = True

            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            left = page_range[(page_number - 4) if (page_number - 4) > 0 else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True

        else:

            left = page_range[(page_number - 4) if (page_number - 4) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 3]

            if right[-1] < total_pages - 1:
                right_has_more = True

            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True

            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data






def logcreate(request,**kwargs):
    if request.method == "GET":
        a=request.path
        user = a.split('.html')[0].split('-')[-1]
        pk = a.split('.html')[0].split('-')[-2]
        kw = a.split('.html')[0].split('-')[1]
        print(pk,kw)
    if kw == 'c':
        str1=str(pk)+'在'+time.strftime("%Y-%m-%d",time.localtime(time.time()))+'被录入'
        # print(str1)
    if kw == 'l':
        str1=str(pk)+'在'+time.strftime("%Y-%m-%d",time.localtime(time.time()))+'被'+user+'领用'

    if kw == 'o':
        str1=str(pk)+'在'+time.strftime("%Y-%m-%d",time.localtime(time.time()))+'被'+user+'借用'

    if kw == 'u':
        str1=str(pk)+'在'+time.strftime("%Y-%m-%d",time.localtime(time.time()))+'信息被修改'

    if kw == 'i':
        str1=str(pk)+'在'+time.strftime("%Y-%m-%d",time.localtime(time.time()))+'归还成功'

    if kw == 'p':
        str1=str(pk)+'在'+time.strftime("%Y-%m-%d",time.localtime(time.time()))+'报废'

    print(pk, str1)
    try:
        user = request.user.username
        models.tb_log.objects.create(uid_id=pk, log_info=str1, user=user)
    except BaseException :
            return HttpResponse('数据录入成功，操作日志录入失败，请联系开发人员')
    else:
        return HttpResponseRedirect(reverse_lazy('assets:assets_list'))

