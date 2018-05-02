import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View

from xiaoi_ops import settings
from .form import *


# 人员管理视图
# Create your views here.
class PersonAdd(LoginRequiredMixin, CreateView):
    """增加"""
    model = person
    form_class = PersonForm
    template_name = 'base_info/person/person-add-update.html'
    success_url = reverse_lazy('base-info:person_list')


class PersonList(LoginRequiredMixin, ListView):
    model = person
    template_name = 'base_info/person/person.html'
    context_object_name = "person_list"
    paginate_by = settings.DISPLAY_PER_PAGE


class PersonUpdate(LoginRequiredMixin, UpdateView):
    model = person
    success_url = reverse_lazy('base-info:person_list')
    form_class = PersonForm
    template_name = 'base_info/person-add-update.html'


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
            # class PartAdd(LoginRequiredMixin, CreateView):
            #     """增加"""
            #     model = person
            #     form_class = PersonForm
            #     template_name = 'base_info/person/person-add-update.html'
            #     success_url = reverse_lazy('base-info:person_list')
            #
            #
            # class PartList(LoginRequiredMixin,ListView):
            #
            #     model = person
            #     template_name = 'base_info/person/person.html'
            #     context_object_name = "person_list"
            #     paginate_by = settings.DISPLAY_PER_PAGE
            #
            #
            # class PartUpdate(LoginRequiredMixin,UpdateView):
            #
            #     model = person
            #     success_url = reverse_lazy('base-info:person_list')
            #     form_class = PersonForm
            #     template_name = 'base_info/person/person-add-update.html'
            #
            #
            # class PartDel(LoginRequiredMixin,View):
            #     model = person
            #     def post(self,request):
            #         ret = {'status':True,'error':None}
            #         try:
            #             if request.POST.get('nid'):
            #                 id = request.POST.get('nid',None)
            #                 person.objects.get(id=id).delete()
            #             else:
            #                 ids = request.POST.getlist('id',None)
            #                 if len(ids) == 0:
            #                     ret['status'] = False
            #                     ret['error'] = '请选者删除的条目'
            #                 else:
            #                     idstring = ','.join(ids)
            #                     person.objects.extra(where=['id IN ('+ idstring+')']).delete()
            #         except Exception as e:
            #             ret['status'] = False
            #             ret['error'] = '删除错误'.format(e)
            #         finally:
            #             return HttpResponse(json.dumps(ret))

            #商家管理视图
