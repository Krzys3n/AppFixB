from django import forms
from .models import App,Report


class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ['name', 'description']
        labels = {'description': 'Opis Aplikacji', 'name': 'Nazwa Aplikacji'}


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['content']
        labels = {}



