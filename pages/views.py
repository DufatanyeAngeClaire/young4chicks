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
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

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
    query = request.GET.get('q')
    if query:
        farmers = Farmer.objects.filter(
            Q(farmer_name__icontains=query) |
            Q(farmer_nin__icontains=query) |
            Q(farmer_type__icontains=query)
        )
    else:
        farmers = Farmer.objects.all()
    return render(request, 'pages/farmers_list.html', {'farmers': farmers})

def edit_farmer(request, id):
    farmer = get_object_or_404(Farmer, id=id)
    form = FarmerRegistrationForm(request.POST or None, instance=farmer)
    if form.is_valid():
        form.save()
        return redirect('farmers_list')
    return render(request, 'pages/register_farmer.html', {'form': form})

def delete_farmer(request, id):
    farmer = get_object_or_404(Farmer, id=id)
    farmer.delete()
    return redirect('farmers_list')

def request_chicks(request, id):
    farmer = get_object_or_404(Farmer, id=id)
    # You can store farmer ID in session or pass via GET to prefill request form
    return redirect('record_requests')  # Or pass data via query params

@login_required
def register_farmer(request, id=None):
    farmer = Farmer.objects.get(pk=id) if id else None
    form = FarmerRegistrationForm(request.POST or None, instance=farmer)
    if form.is_valid():
        form.save()
        return redirect('farmers_list')
    return render(request, 'pages/register_farmer.html', {'form': form})



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
     from django.http import HttpResponse


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
def register_farmer(request, id=None):
    farmer = None
    if id:
        farmer = get_object_or_404(Farmer, id=id)

    farmer = Farmer.objects.get(pk=id) if id else None
    form = FarmerRegistrationForm(request.POST or None, instance=farmer)
    if form.is_valid():
        form.save()
        return redirect('farmers_list')
    return render(request, 'pages/register_farmer.html', {'form': form})







