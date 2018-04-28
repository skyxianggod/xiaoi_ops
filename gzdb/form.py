from    django import forms

from    gzdb.models import gzdb


class GzdbForm(forms.ModelForm):
    class Meta:
        model = gzdb
        fields = ['type', 'type_size', 'id', 'uid', 'sn', 'stat', 'depart', 'addr', 'user', 'ps', 'history']
        # fields = [
        #     'hostname', 'network_ip', 'inner_ip','system','cpu',
        #     'memory','disk','project','platform','region','manager',
        #     'use','ctime','logintype','ps', 'utime','gtime','otime',
        #     'platform_size','power','UID','PID','netinfo',
        # ]

        labels = {
            "type": "类型",
        }
        # widgets = {
        #     'ps': forms.Textarea(
        #         attrs={'cols': 80, 'rows': 3}),
        #     'platform': forms.Select(
        #         attrs={'class': 'select2',
        #                'data-placeholder': ('----请选择机器类型----')}),
        #     'manager': forms.Select(
        #         attrs={'class': 'select2',
        #                'data-placeholder': ('----请选择负责人----')}),
        #     'region': forms.Select(
        #         attrs={'class': 'select2',
        #                'data-placeholder': ('----请选择区域----')}),
        #     'project': forms.Select(
        #         attrs={'class': 'select2',
        #                'data-placeholder': ('----请选择项目----')}),
        # }

        help_texts = {
            'Id': '*  必填项目,编号唯一',

        }
