from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Userprofile  # my user model is named Userprofile

class SignupForm(UserCreationForm):
    class Meta:
        model = Userprofile
        fields = ['username', 'email', 'password1', 'password2', 'user_type']  # adjust to your fields
