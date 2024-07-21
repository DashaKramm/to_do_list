from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from webapp.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'description': widgets.Textarea(attrs={"cols": 24, "rows": 5}),
            'start_date': widgets.DateInput(attrs={"type": "date"}),
            'end_date': widgets.DateInput(attrs={"type": "date"}),
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 10:
            raise ValidationError('Название должно содержать не менее 10 символов')
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        if description and len(description) < 15:
            raise ValidationError('Описание должно содержать не менее 15 символов')
        return description
