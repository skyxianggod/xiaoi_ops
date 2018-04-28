from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .form import *


# Create your views here.
class PersonAdd(LoginRequiredMixin, CreateView):
    """资产增加"""
    model = person
    form_class = PersonForm
    template_name = 'base_info/person/person-add-update.html'
    success_url = reverse_lazy('cmdb:cmdb_list')
