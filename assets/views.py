from django.shortcuts import render,get_object_or_404
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

class AssetsList(LoginRequiredMixin,ListView):
    template_name = 'assets/assets.html'
    model = assets
    context_object_name = 'assets_list'
    paginate_by = settings.DISPLAY_PER_PAGE
    ordering = ("uid")

    def get_queryset(self):
        if self.request.GET.get('name'):
            query = self.request.GET.get('name', None)
            print(query)
            try:
                queryset =super().get_queryset().filter(Q(user=query)|Q(uid=query))
                print("转换正常了")
            except BaseException:
                queryset =super().get_queryset().filter(Q(user=query))


                print("转换异常了")
        else:
            queryset = super().get_queryset()
        return queryset




class AssetsAdd(LoginRequiredMixin, CreateView):
    """增加"""
    model = assets
    form_class = AssetsForm
    template_name = 'assets/assets-add-update.html'
    success_url = reverse_lazy('assets:assets_list')

    def post(self, request, *args, **kwargs):
        print(self.request.POST)
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

    model = assets
    form_class = AssetsForm_give
    template_name = 'assets/assets-add-update-give.html'
    success_url = reverse_lazy('assets:assets_list')

    def post(self, request, *args, **kwargs):
        b=self.request.path
        a=self.request.POST.copy()
        ret=re.search('-g-',b)
        if ret is None:
            a['active']=3
        else:
            a['active']=2
        # print(a)
        self.request.POST=a
        return super().post(request, *args, **kwargs)


class AssetsUpdatein(LoginRequiredMixin,UpdateView):

    model = assets
    form_class = AssetsForm_in
    template_name = 'assets/assets-add-update-in.html'
    success_url = reverse_lazy('assets:assets_list')

    def post(self, request, *args, **kwargs):
        a=self.request.POST.copy()
        a['active']=1
        a['user']=''
        a['otime']=''
        print(a)
        self.request.POST=a
        return super().post(request, *args, **kwargs)






