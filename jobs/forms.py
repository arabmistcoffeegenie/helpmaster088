from django import forms
from .models import CVUpload  # Ensure this imports the correct model

class CVUploadForm(forms.ModelForm):
    class Meta:
        model = CVUpload  # Use the CVUpload model which has the 'cv' field
        fields = ['cv']
