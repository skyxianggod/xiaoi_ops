from django import forms

from work_order.models import *

class OrderForm(forms.ModelForm):


    class Meta:
        model = order
        fields = '__all__'


        widgets = {
            'event_ps': forms.Textarea(
                    attrs={'cols': 80, 'rows': 3}),

            'event_starttime': forms.DateInput(
                attrs={'type': 'date', }
            ),
            'event_endtime': forms.DateInput(
                attrs={'type': 'date', }
            ),
        }

        help_texts = {
            'event_name': '*  必填项目',
            'event_ps': '*  必填项目',
            'event_starttime': '*  必填项目',
            'event_endtime': '*  必填项目',
            'event_status': '*  必填项目',
            'person': '*  必填项目',
        }
