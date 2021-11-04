from django import forms
from .models import Organization, User, Image
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
    The form for new user registration
    """
    class Meta:
        model = Image
        fields = ['image_name', 'image_description', 'group', 'image_upload']

class UserLoginForm(AuthenticationForm):
    '''
    The form for user login
    '''
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                _("This account is inactive."),
                code='inactive',
            )
