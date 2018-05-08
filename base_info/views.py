import json
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View

from xiaoi_ops import settings
from .form import *
from django.db.models import Q
from .models import *

# 人员管理视图
# Create your views here.
class PersonAdd(LoginRequiredMixin, CreateView):
    """增加"""
    model = person
    form_class = PersonForm
    template_name = 'base_info/person/person-add-update.html'
    success_url = reverse_lazy('base_info:person_list')


class PersonList(LoginRequiredMixin, ListView):
    model = person
    template_name = 'base_info/person/person.html'
    context_object_name = "person_list"
    paginate_by = settings.DISPLAY_PER_PAGE
    ordering = ("id")

    def get_queryset(self):
        if self.request.GET.get('name'):
            query = self.request.GET.get('name', None)
            queryset =super().get_queryset().filter(Q(name=query) | Q(id=query) |Q(part=query)).order_by('-id')
        else:
            queryset = super().get_queryset()
        return queryset



class PersonUpdate(LoginRequiredMixin, UpdateView):
    model = person
    success_url = reverse_lazy('base_info:person_list')
    form_class = PersonForm
    template_name = 'base_info/person/person-add-update.html'


class PersonDel(LoginRequiredMixin, View):
    model = person

    def post(self, request):
        ret = {'status': True, 'error': None}
        try:
            if request.POST.get('nid'):
                id = request.POST.get('nid', None)
                person.objects.get(id=id).delete()
            else:
                ids = request.POST.getlist('id', None)
                if len(ids) == 0:
                    ret['status'] = False
                    ret['error'] = '请选者删除的条目'
                else:
                    idstring = ','.join(ids)
                    person.objects.extra(where=['id IN (' + idstring + ')']).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除错误'.format(e)
        finally:
            return HttpResponse(json.dumps(ret))


# 部门管理视图
class PartAdd(LoginRequiredMixin, CreateView):
    """增加"""
    model = department
    form_class = DepartmentForm
    template_name = 'base_info/department/department-add-update.html'
    success_url = reverse_lazy('base_info:part_list')


class PartList(LoginRequiredMixin, ListView):
    model = department
    template_name = 'base_info/department/department.html'
    context_object_name = "part_list"
    paginate_by = settings.DISPLAY_PER_PAGE
    ordering = ("id")

    def get_queryset(self):
        if self.request.GET.get('name'):
            query = self.request.GET.get('name', None)
            queryset =super().get_queryset().filter(Q(name=query) | Q(id=query) |Q(part=query)).order_by('-id')
        else:
            queryset = super().get_queryset()
        return queryset



class PartUpdate(LoginRequiredMixin, UpdateView):
    model = department
    success_url = reverse_lazy('base_info:department_list')
    form_class = DepartmentForm
    template_name = 'base_info/department/department-add-update.html'


class PartDel(LoginRequiredMixin, View):
    model = department

    def post(self, request):
        ret = {'status': True, 'error': None}
        try:
            if request.POST.get('nid'):
                id = request.POST.get('nid', None)
                department.objects.get(id=id).delete()
            else:
                ids = request.POST.getlist('id', None)
                if len(ids) == 0:
                    ret['status'] = False
                    ret['error'] = '请选者删除的条目'
                else:
                    idstring = ','.join(ids)
                    department.objects.extra(where=['id IN (' + idstring + ')']).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除错误'.format(e)
        finally:
            return HttpResponse(json.dumps(ret))

#商家管理视图
class ShopAdd(LoginRequiredMixin, CreateView):
    """增加"""
    model = shop
    form_class = ShopForm
    template_name = 'base_info/shop/shop-add-update.html'
    success_url = reverse_lazy('base_info:shop_list')


class ShopList(LoginRequiredMixin, ListView):
    model = shop
    template_name = 'base_info/shop/shop.html'
    context_object_name = "shop_list"
    paginate_by = settings.DISPLAY_PER_PAGE
    ordering = ("id")




class ShopUpdate(LoginRequiredMixin, UpdateView):
    model = shop
    success_url = reverse_lazy('base_info:shop_list')
    form_class = ShopForm
    template_name = 'base_info/shop/shop-add-update.html'


class ShopDel(LoginRequiredMixin, View):
    model = shop

    def post(self, request):
        ret = {'status': True, 'error': None}
        try:
            if request.POST.get('nid'):
                id = request.POST.get('nid', None)
                shop.objects.get(id=id).delete()
            else:
                ids = request.POST.getlist('id', None)
                if len(ids) == 0:
                    ret['status'] = False
                    ret['error'] = '请选者删除的条目'
                else:
                    idstring = ','.join(ids)
                    shop.objects.extra(where=['id IN (' + idstring + ')']).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除错误'.format(e)
        finally:
            return HttpResponse(json.dumps(ret))


#设备类型视图
#
class PlatformList(ListView):
    template_name = 'base_info/platform/platform.html'
    context_object_name = "dic_list"
    paginate_by = settings.DISPLAY_PER_PAGE

    def get_queryset(self):

        dic_list=[]
        P = platform.objects.all()
        # S = platform_size.objects.all()
        for i in P:
            L = []
            dic = {}
            S = platform_size.objects.filter(platform__name=i.name)
            for x in S:
                L.append(x.name)
            dic[i.name] = L
            dic_list.append(dic)
        print(dic_list)
        # return render(request, 'base_info/platform/platform.html', {'dic': dic})
        return dic_list






