from django.shortcuts import render,HttpResponse
import json

# Create your views here.
from xiaoi_ops import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,TemplateView,ListView,View,UpdateView
from .models import pfdb
from .form import PfdbFrom
from django.urls import reverse_lazy

class PlatfromList(ListView,LoginRequiredMixin):
    model = pfdb
    template_name = 'pfdb/pfdb.html'
    paginate_by = settings.DISPLAY_PER_PAGE
    context_object_name = 'pfdb_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            "platform_class": 'active',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

class PlatfromCreat(LoginRequiredMixin,CreateView):
    model = pfdb
    success_url = reverse_lazy('pfdb:pfdb_list')
    form_class = PfdbFrom
    template_name = 'pfdb/pfdb-add-update.html'

class PlatfromUpdate(LoginRequiredMixin,UpdateView):

    model = pfdb
    success_url = reverse_lazy('pfdb:pfdb_list')
    form_class = PfdbFrom
    template_name = 'pfdb/pfdb-add-update.html'
    
    
class PfdbDel(LoginRequiredMixin,View):
    model = pfdb
    def post(self,request):
        ret = {'status':True,'error':None}
        try:
            if request.POST.get('nid'):
                id = request.POST.get('nid',None)
                pfdb.objects.get(id=id).delete()
            else:
                ids = request.POST.getlist('id',None)
                if len(ids) == 0:
                    ret['status'] = False
                    ret['error'] = '请选者删除的条目'
                else:
                    idstring = ','.join(ids)
                    pfdb.objects.extra(where=['id IN ('+ idstring+')']).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除错误'.format(e)
        finally:
            return HttpResponse(json.dumps(ret))





