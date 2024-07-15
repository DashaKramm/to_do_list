from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

from webapp.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'description': widgets.Textarea(attrs={"cols": 24, "rows": 5}),
            'type': widgets.CheckboxSelectMultiple(),
        }

    def clean_summary(self):
        summary = self.cleaned_data['summary']
        if len(summary) < 10:
            raise ValidationError('Краткое описание должно содержать не менее 10 символов')
        return summary

    def clean_description(self):
        description = self.cleaned_data['description']
        if description and len(description) < 15:
            raise ValidationError('Полное описание должно содержать не менее 15 символов')
        return description


class TaskDeleteForm(forms.Form):
    tasks = forms.ModelMultipleChoiceField(
        queryset=Task.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
