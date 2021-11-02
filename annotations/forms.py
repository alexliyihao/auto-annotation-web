from django import forms
from .models import Organization,User
from datetime import datetime

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'UNI', 'organizations']
