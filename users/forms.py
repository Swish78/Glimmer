from django import forms
from .models import CustomUser

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'city', 'state', 'country', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'cols': 20, 'rows': 2})
        }


class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['phone_number', 'city', 'state', 'country', 'address']
