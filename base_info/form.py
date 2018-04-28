import re

from django import forms

from .models import department, person, shop


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = department
        fields = '__all__'
        help_texts = {
            'id': '*  唯一编号',
            'name': '*  必填项目',
        }


class ShopForm(forms.ModelForm):
    class Meta:
        model = shop
        fields = '__all__'
        help_texts = {
            'user': '*  必填项目',
            'name': '*  必填项目',
            'mobile': '*  必填项目'
        }


class PersonForm(forms.ModelForm):
    # def __init__(self,*args,**kwargs):
    #     super(PersonForm,self).__init__(*args,**kwargs)
    #     self.a=[(i.name,i.name) for i in department.objects.all()]
    #     print(self.a)
    #     person.part['cho']


    part = forms.ModelChoiceField(label='部门', queryset=department.objects.all())

    # queue = forms.ModelChoiceField(label=u'队列',queryset=Queue.objects.all())
    class Meta:
        model = person
        fields = '__all__'
        # exclude = ['part']
        help_texts = {
            'id': '*  必填项目',
            'name': '*  必填项目',
            'part': '*  必填项目',
            'mobile': '*  必填项目',
        }

    def clean_mobile(self):  # 函数必须以clean_开头
        """
        通过正则表达式验证手机号码是否合法
        """
        mobile = self.cleaned_data['mobile']
        mobile_regex = r'^1[34578]\d{9}$'
        p = re.compile(mobile_regex)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法', code='invalid mobile')
