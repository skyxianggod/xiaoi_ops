from django.shortcuts import render,get_object_or_404

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View
from xiaoi_ops import settings
from  .models import *
from .form import AssetsForm,AssetsForm_give
from django.core import serializers

class AssetsList(LoginRequiredMixin,ListView):
    template_name = 'assets/assets.html'
    model = assets
    context_object_name = 'assets_list'
    paginate_by = settings.DISPLAY_PER_PAGE
    ordering = ("uid")


class AssetsAdd(LoginRequiredMixin, CreateView):
    """增加"""
    model = assets
    form_class = AssetsForm
    template_name = 'assets/assets-add-update.html'
    success_url = reverse_lazy('assets:assets_list')

def getdata(request):
    pk = request.GET['pk']
    plat = get_object_or_404(platform, pk=pk)
    size = plat.platform_size_set.all()
    data = serializers.serialize('json', size)
    print(data)
    return HttpResponse(data, content_type='application/json')

class AssetsUpdate(LoginRequiredMixin,UpdateView):

    model = assets
    form_class = AssetsForm_give
    template_name = 'assets/assets-add-update-give.html'
    success_url = reverse_lazy('assets:assets_list')

    def post(self, request, *args, **kwargs):

        pk = self.request.GET.get('pk')
        print(pk)
        q = assets.objects.get(uid=pk)
        q.active=2
        q.save()
        print(1)
        return super().post(self, request, *args, **kwargs)
        # return HttpResponse('200')



