from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form_data = UserCreationForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            username = form_data.cleaned_data.get('username')
            email = form_data.cleaned_data.get('email')
            return redirect('/login')
    else:
        form_data = UserCreationForm()
    return render(request, 'pages/signup.html', {'form_data': form_data})