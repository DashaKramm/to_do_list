from django import forms

from webapp.models import Task


class TaskDeleteForm(forms.Form):
    tasks = forms.ModelMultipleChoiceField(
        queryset=Task.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
