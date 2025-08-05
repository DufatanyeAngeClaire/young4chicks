from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import SignupForm
from django.contrib.auth import get_user_model
from .models import  Chickrequest
from django.contrib.auth import login

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form_data = SignupForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            return redirect('login')
    else:
        form_data = SignupForm()
    
    return render(request, 'pages/signup.html', {'form': form_data})

def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.user_type == 'sales_agent':
                login(request, user)
                return redirect('/salesagent')

            elif user.user_type == 'manager':
                login(request, user)
                return redirect('/manager')
    form = AuthenticationForm()
    return render(request, 'pages/login.html', {'form': form, 'title': 'Login'})
def homepage(request):
#    requests_data = request.objects.all().order_by('date').filter( request.chick_status == 'Pending')
 requests_data = Chickrequest.objects.filter(chick_status='Pending').order_by('chick_date')

 context = {
     'request' : requests_data
   }
 return render(request, 'pages/index.html', context)

def manager_dashboard(request):
    return render(request, 'pages/manager.html')
