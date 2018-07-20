
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import ListView

from xiaoi_ops import settings
from .models import *


class AssetsList(LoginRequiredMixin,ListView):
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
        if self.request.GET.get('name'):
            query = self.request.GET.get('name', None)
            # print(query)
            try:
                queryset = super().get_queryset().filter(
                        Q(user__icontains=query) | Q(uid__icontains=query) | Q(active_id__icontains=query) | Q(
                            pid__icontains=query)).order_by('pid')
                # print('......')
            except BaseException as e:
                # print(e)
                queryset = super().get_queryset().filter(
                    Q(user__icontains=query) | Q(uid__icontains=query) | Q(pid__icontains=query)).order_by('pid')
        else:
            queryset = super().get_queryset()
        return queryset


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