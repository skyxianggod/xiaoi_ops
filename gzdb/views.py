# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from gzdb.models import gzdb
from xiaoi_ops import settings
from .form import GzdbForm


class GzdbListAll(LoginRequiredMixin, ListView):
    template_name = 'gzdb/gzdb.html'
    paginate_by = settings.DISPLAY_PER_PAGE
    model = gzdb
    context_object_name = "gzdb_list"
    ordering = ("id")


class GzdbCreate(LoginRequiredMixin, CreateView):
    """资产增加"""
    model = gzdb
    form_class = GzdbForm
    template_name = 'gzdb/gzdb-add-update.html'
    success_url = reverse_lazy('gzdb:gzdb_list')
