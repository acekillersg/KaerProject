from django import forms
from django.forms import ModelForm
from Storage.models import PageToRender


class PageToRenderForm(ModelForm):
    class Meta:
        model = PageToRender
        exclude = ["page_name", "from_date", "from_time", "to_date", "to_time"]
        # exclude = ["page_name"]
        widgets = {
            'from_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'from_time': forms.TimeInput(attrs={'class': 'datepicker'}),
            'to_date': forms.DateInput(attrs={'class': 'datepicker'}),
            'to_time': forms.TimeInput(attrs={'class': 'datepicker'}),
        }