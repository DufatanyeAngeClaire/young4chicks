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
from .forms import ChickrequestForm 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ChickrequestForm
from .forms import FarmerRegistrationForm
from .models import Farmer


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
                return redirect('/saleagent')

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

def logout(request):
    return render(request, 'pages/index.html')

def manager_dashboard(request):
    return render(request, 'pages/manager.html')

def salesagent(request):
    return render(request, 'pages/sales_agent.html')
def farmer_dashboard(request):
    return render(request, 'pages/farmer.html')
def my_requests(request):
    return render(request, 'pages/my_requests.html')
def profile_view(request):
    return render(request, 'pages/profile.html')
def stock(request):
    return render(request, 'pages/stock.html')
def approve_requests(request):
    return render(request, 'pages/approve_requests.html')


def farmers_list(request):
    farmers = Farmer.objects.all()
    return render(request, 'pages/farmers_list.html', {'farmers': farmers})

def approved_sales(request):
    return render(request, 'pages/approved_sales.html')

@login_required
def record_requests(request):
    try:
        # Try to get the farmer linked to the current user
        farmer = Farmer.objects.get(farmer_name=request.user)
    except Farmer.DoesNotExist:
        farmer = None

    # If no farmer profile is found, redirect or show error
    if not farmer:
        return render(request, 'pages/error.html', {
            'message': 'You must register as a farmer before making a request.'
        })

    if request.method == 'POST':
        form = ChickrequestForm(request.POST, farmer=farmer)
        if form.is_valid():
            chick_request = form.save(commit=False)
            chick_request.farmer_name = farmer  # Assign farmer manually
            chick_request.save()
            return redirect('my_requests')  # Redirect to request history page
    else:
        form = ChickrequestForm(farmer=farmer)

    return render(request, 'pages/record_requests.html', {'form': form})


@login_required
def register_farmer(request):
    if request.method == 'POST':
        form = FarmerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('farmers_list')  # Or wherever you want after registration
    else:
        form = FarmerRegistrationForm()
    return render(request, 'pages/register_farmer.html', {'form': form})

from django.shortcuts import render

def your_view(request):
    user_is_farmer = False
    if request.user.is_authenticated:
        # Check if Farmer object exists for this user
        user_is_farmer = hasattr(request.user, 'farmer')

    context = {
        'user_is_farmer': user_is_farmer,
        'message': 'Your message here',
    }
    return render(request, 'pages/error.html', context)



