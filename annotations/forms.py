from django import forms
from .models import Organization
from datetime import datetime

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
                        max_length = 40,
                        label = 'Username',
                        required = True,
                        initial = 'username'
                        )
    # The password
    password = forms.CharField(
                        max_length = 40,
                        label = 'Password',
                        required = True,
                        widget=forms.PasswordInput()
                        )
    # The legal Name
    first_name = forms.CharField(
                        max_length = 40,
                        label = 'First name',
                        required = True,
                        initial = 'first name'
                        )
    # The legal Name
    last_name = forms.CharField(
                        max_length = 40,
                        label = "Last name",
                        required = True,
                        initial = 'last_name'
                        )
    # User's email
    email = forms.EmailField(
                        label = "Email",
                        required = True,
                        initial = 'examples@columbia.edu'
                        )
    # UNI
    UNI = forms.CharField(
                        max_length = 8,
                        label = "UNI",
                        required = True
                        )
    register_date = forms.DateTimeField(
                        initial = datetime.now()
                        disabled = True
                        )
                        
    # The organization this user belongs to
    organizations = forms.ModelChoiceField(
                        queryset = Organization.objects.all()
                        label = 'Organization',
                        empty_label="not in the list",
                        required = True,
                        to_field_name = "organization_name"
                        )
