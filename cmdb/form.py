from    django import forms

from    cmdb.models import cmdb


class CmdbForm(forms.ModelForm):

    class Meta:
        model = cmdb
        # fields = '__all__'
        fields = [
            'hostname', 'network_ip', 'inner_ip','system','cpu',
            'memory','disk','project','platform','region','manager',
            'use','ctime','logintype','ps', 'utime','gtime','otime',
            'platform_size','power','UID','PID','netinfo',
        ]

        labels = {
            "network_ip": "外网IP",
        }
        widgets = {
            'ps': forms.Textarea(
                attrs={'cols': 80, 'rows': 3}),
            'platform': forms.Select(
                attrs={'class': 'select2',
                       'data-placeholder': ('----请选择机器类型----')}),
            'manager': forms.Select(
                attrs={'class': 'select2',
                       'data-placeholder': ('----请选择负责人----')}),
            'region': forms.Select(
                attrs={'class': 'select2',
                       'data-placeholder': ('----请选择区域----')}),
            'project': forms.Select(
                attrs={'class': 'select2',
                       'data-placeholder': ('----请选择项目----')}),

            'otime': forms.DateInput(
                attrs={'type': 'date', }
            ),
            'gtime': forms.DateInput(
                attrs={'type': 'date', }
            ),
            'ctime': forms.DateInput(
                attrs={'type': 'date', }
            ),
            'utime': forms.DateInput(
                attrs={'type': 'date', }
            ),
        }

        help_texts = {
            'hostname': '*  必填项目,名字唯一',
            'platform': '*  必填项目',
            'region': '*  必填项目',
            'manager': '*  必填项目',
            'project': '*  必填项目'
        }
        error_messages = {
            'model': {
                'max_length': ('太短了'),
            }
        }

class FileForm(forms.Form):
    file = forms.FileField(label="资产导入")