#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms

from assets.models import *


class AssetsForm(forms.ModelForm):


    class Meta:
        model = assets
        # fields = '__all__'
        fields = ['uid', 'utype', 'usize', 'ctime', 'addr', 'ps', 'sn', 'pid', 'nmac', 'wmac', 'upart', 'cpu', 'mem',
                  'disk'
                  ]


        widgets = {
            'ps': forms.Textarea(
                    attrs={'cols': 80, 'rows': 3}),

            # 'utpye': forms.ModelChoiceField(
            #     attrs={'id': 'utype_id',}),

            'otime': forms.DateInput(
                attrs={'type': 'date', }
            ),
            'gtime': forms.DateInput(
                attrs={'type': 'date', }
            ),
            'ctime': forms.DateInput(
                attrs={'type': 'date', }
            ),
        }
        #
        # help_texts = {
        #     'hostname': '*  必填项目,名字唯一',
        #     'platform': '*  必填项目',
        #     'region': '*  必填项目',
        #     'manager': '*  必填项目',
        #     'project': '*  必填项目'
        # }
        # error_messages = {
        #     'model': {
        #         'max_length': ('太短了'),
        #     }
        # }
class AssetsForm_give(forms.ModelForm):

    user = forms.CharField(max_length=24,label="用户")

    class Meta:
        model = assets
        # fields = '__all__'
        fields = ['otime', 'user', 'active', 'gtime', 'addr', 'ps', 'upart'
                  ]


        widgets = {
            'ps': forms.Textarea(
                attrs={'cols': 80, 'rows': 3}),

            'otime': forms.DateInput(
                attrs={'type': 'date','required':'True'}
            ),
            'gtime': forms.DateInput(
                attrs={'type': 'date','required':'True'}
            ),
            'ctime': forms.DateInput(
                attrs={'type': 'date', }
            ),
        }


class AssetsForm_in(forms.ModelForm):


    class Meta:
        model = assets
        # fields = '__all__'
        fields = ['otime', 'user', 'active', 'gtime', 'upart'
                  ]


        widgets = {
            'ps': forms.Textarea(
                attrs={'cols': 80, 'rows': 3}),
            # 'utpye': forms.ModelChoiceField(
            #     attrs={'id': 'utype_id',}),

            'otime': forms.DateInput(
                attrs={'type': 'date', }
            ),
            'gtime': forms.DateInput(
                attrs={'type': 'date', }
            ),
            'ctime': forms.DateInput(
                attrs={'type': 'date', }
            ),
        }



