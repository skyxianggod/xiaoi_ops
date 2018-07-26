
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView

from xiaoi_ops import settings
from .form import *
from .models import *


class OrderList(LoginRequiredMixin,ListView):
    template_name = 'work_order/order.html'
    model = order
    context_object_name = 'order_list'
    paginate_by = settings.DISPLAY_PER_PAGE
    ordering = ("-id")


    def get_context_data(self, *, object_list=None, **kwargs):

        search_data = self.request.GET.copy()
        # print(search_data)
        # 高级分页
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')

        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator, page, is_paginated)
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
            "order_class": 'active',
        }
        kwargs.update(context)
        kwargs.update(pagination_data)
        return super().get_context_data(**kwargs)



    def get_queryset(self):

        if self.request.GET.get('name') or self.request.GET.get('status') or self.request.GET.get('stime') or self.request.GET.get('etime'):
            data = {}
            query_name = self.request.GET.get('name')
            query_status = self.request.GET.get('status')
            query_stime = self.request.GET.get('stime')
            query_etime = self.request.GET.get('etime')
            print(query_name,query_status,query_etime,query_stime)
            if query_status != '':
                data = {'event_status':query_status}
            queryset = super().get_queryset().filter(**data)
            if query_name != '' :
                queryset = queryset.filter(Q(event_name__icontains=query_name) | Q(person=query_name))
                if query_stime != '':
                    queryset = queryset.filter(Q(event_updatetime__gte=query_stime))
                elif query_etime != '':
                    queryset = queryset.filter(Q(event_updatetime__lte=query_etime))

            elif query_stime != '':
                queryset = queryset.filter(Q(event_updatetime__gte=query_stime))
                if query_etime != '':
                    queryset = queryset.filter(Q(event_updatetime__lte=query_etime))
            elif query_etime != '':
                queryset = queryset.filter(Q(event_updatetime__lte=query_etime))


        # if query_name:
        #     query_stime = self.request.GET.get('stime', None)
        #     query_etime = self.request.GET.get('etime', None)
        #     print(self.request.GET)
        #     # print(query)
        #     try:
        #         queryset = super().get_queryset().filter(
        #             Q(event_name__icontains=query_name)  | Q(person=query_name) &
        #             Q(event_status=query_status) & Q(end_time__gte=query_stime) &
        #             Q(end_time__lte=query_etime)).order_by('-id')
        #         # print('......')
        #     except BaseException as e:
        #         # print(e)
        #         pass
        else:
            queryset = super().get_queryset()
        return queryset.order_by('person')


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


class OrderCreate(LoginRequiredMixin, CreateView):
    """增加"""
    model = order
    form_class = OrderForm
    template_name = 'work_order/order-add-update.html'
    success_url = reverse_lazy('order:order_list')


class OrderUpdate(LoginRequiredMixin, UpdateView):
    model = order
    form_class =  Order2Form
    template_name = 'work_order/order-add-update.html'
    # context_object_name = 'obj'
    success_url = reverse_lazy('order:order_list')


