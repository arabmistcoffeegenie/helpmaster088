from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class DarkAuthForm(AuthenticationForm):
    """
    Custom login form that applies dark styling to username/password fields.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control dark-input',
            'placeholder': 'Username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control dark-input',
            'placeholder': 'Password',
        })

class RegistrationForm(UserCreationForm):
    """
    Custom registration form that applies dark styling to all fields.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control dark-input',
            'placeholder': 'Email',
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control dark-input',
            'placeholder': 'Username',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control dark-input',
            'placeholder': 'Password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control dark-input',
            'placeholder': 'Confirm Password',
        })
