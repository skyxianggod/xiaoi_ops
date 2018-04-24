from django import forms
from .models import pfdb

class PfdbFrom(forms.ModelForm):

    class Meta:
        model = pfdb
        fields = ['platfrom_name','platfrom_url']

        labels = {
            "platfrom_name": "平台名称",
        }
