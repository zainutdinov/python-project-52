from django import forms

from .models import Label


class LabelCreateForm(forms.ModelForm):
    class Meta():
        model = Label
        fields = ['name']
        labels = {'name': 'Имя'}
