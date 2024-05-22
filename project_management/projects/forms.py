from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Task, Project
from django.contrib.auth.models import User

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Project'))

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'project', 'assigned_to', 'due_date', 'status', 'priority']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Task'))
        self.fields['project'].queryset = Project.objects.all()
        self.fields['assigned_to'].queryset = User.objects.all()
