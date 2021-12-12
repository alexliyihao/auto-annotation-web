from django import forms
from .models import Organization, User, Image, Annotation
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm

class UserRegistrationForm(forms.ModelForm):
    """
    The form for new user registration
    """
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'UNI', 'organizations']


class ImageUploadForm(forms.ModelForm):
    """
    The form for image uploading
    """
    class Meta:
        model = Image
        fields = ['image_name', 'image_description', 'group', 'image_upload']

class ImageBatchUploadForm(forms.ModelForm):
    """
    The form for image uploading by batch
    """
    image_upload = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = Image
        fields = ['image_name', 'image_description', 'group', 'image_upload']

class UserLoginForm(AuthenticationForm):
    '''
    The form for user login
    '''
    def confirm_login_allowed(self, user):
        pass

class AnnotationCreateform(forms.ModelForm):
    '''
    The form for submitting annotations
    '''
    class Meta:
        model = Annotation
        fields = ['contour', "image", "annotator"]
