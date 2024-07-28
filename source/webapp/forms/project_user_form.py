from django import forms
from django.contrib.auth import get_user_model

from webapp.models import Project

User = get_user_model()


class ProjectUserForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Project
        fields = ['users']
