from django import forms
from .models import Organization, User, Image
from datetime import datetime

class UserRegistrationForm(forms.ModelForm):
    """
    The form for new user registration
    """
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'UNI', 'organizations']


class ImageUploadForm(forms.ModelForm):
    """
    The form for new user registration
    """
    class Meta:
        model = Image
        fields = ['image_name', 'image_description', 'group', 'image_upload']
