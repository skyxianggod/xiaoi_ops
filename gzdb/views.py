# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from gzdb.models import gzdb
from xiaoi_ops import settings


class GzdbListAll(LoginRequiredMixin, ListView):
    template_name = 'gzdb/gzdb.html'
    paginate_by = settings.DISPLAY_PER_PAGE
    model = gzdb
    context_object_name = "gzdb_list"
    ordering = ("id")
