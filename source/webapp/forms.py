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
            'status': widgets.CheckboxSelectMultiple(),
            'type': widgets.CheckboxSelectMultiple(),
        }

    def clean_summary(self):
        summary = self.cleaned_data['summary']
        if len(summary) < 10:
            raise ValidationError('Краткое описание должно содержать не менее 10 символов')
        return summary

    def clean(self):
        summary = self.cleaned_data.get('summary')
        description = self.cleaned_data.get('description')
        if summary and description and summary == description:
            raise ValidationError('Краткое описание не должно совпадать с полным описанием')
        return super().clean()


class TaskDeleteForm(forms.Form):
    tasks = forms.ModelMultipleChoiceField(
        queryset=Task.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
