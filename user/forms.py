from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from django.forms import PasswordInput, EmailInput



class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'image']

    def clean_email(self):
        email = self.cleaned_data['email']

        try:
            account = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(f'Email {email} is already in user')

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            account = User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(f'Username {username} is already in user')
