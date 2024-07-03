from django import forms
from django.forms import widgets

from webapp.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'detailed_description': widgets.Textarea(attrs={"cols": 24, "rows": 5}),
            'date_of_completion': widgets.DateInput(attrs={"type": "date"}),
        }


class TaskDeleteForm(forms.Form):
    tasks = forms.ModelMultipleChoiceField(
        queryset=Task.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
