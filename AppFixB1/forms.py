from datetime import datetime

from django import forms
from django.db import models

from .models import App, Report, Company

from django import forms
from .models import App

from django import forms
from .models import App

from django import forms
from .models import App

from django import forms
from .models import App

class AppForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('Desktop App', 'Desktop App'),
        ('Web App', 'Web App'),
        ('Game', 'Game'),
        ('Mobile App', 'Mobile App'),
        ('other', 'Other'),
    ]

    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    custom_category = forms.CharField(required=False, label = "" )

    class Meta:
        model = App
        fields = ['name', 'description', 'category', 'custom_category', 'price', 'version', 'access']
        labels = {
            'name': 'App Name',
            'description': 'App Description',
            'category': 'Category:',
            'custom_category': '',
            'price': 'Price',
            'version': 'Version',
            'access': 'Acces',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['class'] = 'inline-select'
        self.fields['custom_category'].widget.attrs['class'] = 'inline-input'
        self.fields['custom_category'].widget.attrs['placeholder'] = 'Input your own app category'
        self.fields['custom_category'].widget.attrs['style'] = 'display:none;'
        self.fields['category'].widget.attrs['onchange'] = 'toggleCustomCategory()'

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        custom_category = cleaned_data.get('custom_category')
        if category == 'other':
            self.fields['custom_category'].widget.attrs['style'] = 'display:true;'
        if category == 'other' and custom_category:

            category = custom_category  # Użyj wprowadzonej wartości jako kategorii

        cleaned_data['category'] = category  # Zapisz zaktualizowaną wartość kategorii

        if category == 'other' and not custom_category:
            raise forms.ValidationError('Please enter your own category name.')

        return cleaned_data




class ReportForm(forms.ModelForm):


    class Meta:

        model = Report
        fields = ['name', 'content', 'priority']

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description']



