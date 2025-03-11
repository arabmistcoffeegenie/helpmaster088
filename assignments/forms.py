# assignments/forms.py

from django import forms
from .models import Assignment

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = [
            'title',
            'degree',
            'module',
            'instructions',
            'deadline',
            'brief',           # Include the FileField here if you have it
        ]
