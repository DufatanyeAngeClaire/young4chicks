from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import HttpResponseForbidden

from .models import Chickrequest, Farmer, Stock, Userprofile
from .forms import (
    SignupForm,
    ChickrequestForm,
    FarmerRegistrationForm,
    ChickStockForm,
    ChickRequestApprovalForm,
    StockForm,
)


# -------- AUTH VIEWS --------

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'pages/signup.html', {'form': form})


def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            auth_login(request, user)
            if user.user_type == 'sales_agent':
                return redirect('sales_agent_dashboard')
            elif user.user_type == 'manager':
                return redirect('manager_dashboard')
            else:
                return redirect('homepage')

        messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'pages/login.html', {'form': form, 'title': 'Login'})


def logout(request):
    auth_logout(request)
    return redirect('login')


# -------- DASHBOARD VIEWS --------

@login_required
def dashboard_landing(request):
    user = request.user
    if user.user_type == 'manager':
        return redirect('manager_dashboard')
    elif user.user_type == 'sales_agent':
        return redirect('sales_agent_dashboard')
    else:
        if hasattr(user, 'farmer_profile'):
            return redirect('farmer_dashboard')
        else:
            return render(request, 'pages/need_farmer_registration.html')


@login_required
def homepage(request):
    requests_data = Chickrequest.objects.filter(chick_status='pending').order_by('chick_date')
    return render(request, 'pages/index.html', {'requests': requests_data})


@login_required
def manager_dashboard(request):
    if request.user.user_type != 'manager':
        return redirect('homepage')

    chick_stock = Stock.objects.all()
    pending_requests = Chickrequest.objects.filter(chick_status='pending').order_by('chick_date')
    approved_requests = Chickrequest.objects.filter(chick_status='approved').order_by('-chick_date')

    context = {
        'chick_stock': chick_stock,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
    }
    return render(request, 'pages/manager_dashboard.html', context)


@login_required
def sales_agent_dashboard(request):
    user = request.user
    if user.user_type != 'sales_agent':
        return redirect('login')

    requests = Chickrequest.objects.filter(sales_agent=user).order_by('-chick_date')
    context = {
        'requests': requests,
        'total_requests': requests.count(),
        'approved_count': requests.filter(chick_status='approved').count(),
        'pending_count': requests.filter(chick_status='pending').count(),
    }
    return render(request, 'pages/sales_agent_dashboard.html', context)
# Remove the login_required decorator from farmer_dashboard
def farmer_dashboard(request):
    # Since no login required, user might be anonymous
    if not request.user.is_authenticated:
        # No user, but farmer can access freely, so maybe show general info or limited dashboard
        # Or you can just let them see a basic farmer dashboard without user-specific data
        return render(request, 'pages/farmer_dashboard.html', {
            'farmer': None,
            'chick_requests': []
        })

    # Logged in user path - if you want to support that
    user = request.user
    if not hasattr(user, 'farmer_profile'):
        return render(request, 'pages/farmer_dashboard.html', {
            'farmer': None,
            'chick_requests': []
        })

    farmer = user.farmer_profile
    chick_requests = farmer.chickrequest_set.all().order_by('-chick_date')

    return render(request, 'pages/farmer_dashboard.html', {
        'farmer': farmer,
        'chick_requests': chick_requests,
    })



# -------- FARMER CRUD --------

@login_required
def farmers_list(request):
    query = request.GET.get('q')
    farmers = Farmer.objects.all()
    if query:
        farmers = farmers.filter(
            Q(farmer_name__icontains=query) |
            Q(farmer_nin__icontains=query) |
            Q(farmer_type__icontains=query)
        )
    return render(request, 'pages/farmers_list.html', {'farmers': farmers})


@login_required
def register_farmer(request, id=None):
    farmer = get_object_or_404(Farmer, id=id) if id else None
    if request.method == 'POST':
        form = FarmerRegistrationForm(request.POST, instance=farmer)
        if form.is_valid():
            f = form.save(commit=False)
            if not farmer:
                f.user = request.user
            f.save()
            return redirect('farmers_list')
    else:
        form = FarmerRegistrationForm(instance=farmer)
    return render(request, 'pages/register_farmer.html', {'form': form})


@login_required
def edit_farmer(request, id):
    return register_farmer(request, id=id)


@login_required
def delete_farmer(request, id):
    farmer = get_object_or_404(Farmer, id=id)
    farmer.delete()
    return redirect('farmers_list')


# -------- CHICK REQUEST VIEWS --------

@login_required
def record_request(request, id=None):
    chick_request = get_object_or_404(Chickrequest, id=id) if id else None
    farmer = chick_request.farmer_name if chick_request else None

    if request.method == 'POST':
        form = ChickrequestForm(request.POST, instance=chick_request, farmer=farmer)
        if form.is_valid():
            form.save()
            return redirect('my_requests')
    else:
        form = ChickrequestForm(instance=chick_request, farmer=farmer)

    requests_list = Chickrequest.objects.filter(sales_agent=request.user)

    return render(request, 'pages/record_request.html', {'form': form, 'requests': requests_list})


@login_required
def all_requests(request):
    if request.user.user_type == 'manager':
        requests_list = Chickrequest.objects.all().order_by('-chick_date')
    elif request.user.user_type == 'sales_agent':
        requests_list = Chickrequest.objects.filter(sales_agent=request.user).order_by('-chick_date')
    else:
        return redirect('homepage')

    return render(request, 'pages/all_requests.html', {'requests': requests_list})


@login_required
def approve_request(request, id):
    if request.user.user_type != 'manager':
        messages.error(request, "You do not have permission to approve requests.")
        return redirect('all_requests')

    chick_request = get_object_or_404(Chickrequest, id=id)
    chick_request.chick_status = 'approved'
    chick_request.save()
    messages.success(request, f"Request #{id} approved successfully.")
    return redirect('all_requests')


@login_required
def reject_request(request, id):
    if request.user.user_type != 'manager':
        messages.error(request, "You do not have permission to reject requests.")
        return redirect('all_requests')

    chick_request = get_object_or_404(Chickrequest, id=id)
    chick_request.chick_status = 'rejected'
    chick_request.save()
    messages.success(request, f"Request #{id} rejected.")
    return redirect('all_requests')


@login_required
def my_requests(request):
    if request.user.user_type != 'sales_agent':
        return redirect('homepage')

    # Assign unassigned requests to this sales agent
    Chickrequest.objects.filter(sales_agent=None).update(sales_agent=request.user)

    if request.method == 'POST':
        form = ChickrequestForm(request.POST)
        if form.is_valid():
            my_request = form.save(commit=False)
            my_request.chick_status = 'pending'
            my_request.sales_agent = request.user
            my_request.save()
            messages.success(request, "Request recorded successfully. Please wait for manager approval.")
            return redirect('record_request')
    else:
        form = ChickrequestForm()

    pending_requests = Chickrequest.objects.filter(
        sales_agent=request.user,
        chick_status='pending'
    ).order_by('-id')

    return render(request, 'pages/my_requests.html', {'form': form, 'requests': pending_requests})


@login_required
def edit_request(request, id):
    request_obj = get_object_or_404(Chickrequest, id=id)
    if request.method == 'POST':
        form = ChickrequestForm(request.POST, instance=request_obj)
        if form.is_valid():
            form.save()
            return redirect('record_request')
    else:
        form = ChickrequestForm(instance=request_obj)
    return render(request, 'pages/record_request.html', {'form': form})


@login_required
def delete_request(request, id):
    request_obj = get_object_or_404(Chickrequest, id=id)
    request_obj.delete()
    return redirect('record_request')


@login_required
def send_request(request, request_id):
    chick_request = get_object_or_404(Chickrequest, pk=request_id)
    # Example: mark as sent, adjust this as per your model field
    chick_request.chick_status = 'sent'  # or whatever is correct
    chick_request.save()
    return redirect('requests_list')


# -------- STOCK VIEWS --------

@login_required
def add_or_update_stock(request, stock_id=None):
    if request.user.user_type != 'manager':
        return redirect('homepage')

    stock = get_object_or_404(Stock, pk=stock_id) if stock_id else None

    if request.method == 'POST':
        form = ChickStockForm(request.POST, instance=stock)
        if form.is_valid():
            obj = form.save(commit=False)
            if not stock:
                obj.registered_by = request.user
            obj.save()
            return redirect('manager_dashboard')
    else:
        form = ChickStockForm(instance=stock)

    return render(request, 'pages/stock_form.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'pages/profile.html')


@login_required
def stock(request):
    return render(request, 'pages/stock.html')


@login_required
def approve_requests(request):
    pending_requests = Chickrequest.objects.filter(chick_status='pending')
    return render(request, 'pages/approve_requests.html', {'pending_requests': pending_requests})


@login_required
def approved_sales(request):
    approved_requests = Chickrequest.objects.filter(chick_status='approved')
    return render(request, 'pages/approved_sales.html', {'approved_requests': approved_requests})


@login_required
def requests_list(request):
    all_requests = Chickrequest.objects.all()
    return render(request, 'pages/requests_list.html', {'requests': all_requests})


@login_required
@require_POST
def update_delivery_status(request, pk):
    user = request.user
    if user.user_type != 'sales_agent':
        return HttpResponseForbidden("You do not have permission to perform this action.")

    chick_req = get_object_or_404(Chickrequest, pk=pk, sales_agent=user)
    new_status = request.POST.get('chick_delivered')
    if new_status in ['yes', 'no']:
        chick_req.chick_delivered = new_status
        chick_req.save()

    return redirect('sales_agent_dashboard')

@login_required
def chickrequest_list(request):
    chickrequests = Chickrequest.objects.all()
    return render(request, 'pages/chickrequest_list.html', {'saleagent': chickrequests})


def landing_page(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'manager':
            return redirect('manager_dashboard')
        elif request.user.user_type == 'sales_agent':
            return redirect('sales_agent_dashboard')
        elif hasattr(request.user, 'farmer_profile'):
            return redirect('farmer_dashboard')
    # Else, show public requests page
    return public_farmer_requests(request)
    
def logout(request):
    auth_logout(request)
    return redirect('landing_page')

def public_farmer_requests(request):
    search_query = request.GET.get('q', '')

    # Filter requests by search query if provided
    if search_query:
        approved_requests = Chickrequest.objects.filter(
            Q(chick_status='approved'),
            Q(farmer_name__icontains=search_query)
        ).order_by('-chick_date')

        pending_requests = Chickrequest.objects.filter(
            Q(chick_status='pending'),
            Q(farmer_name__icontains=search_query)
        ).order_by('-chick_date')
    else:
        approved_requests = Chickrequest.objects.filter(chick_status='approved').order_by('-chick_date')
        pending_requests = Chickrequest.objects.filter(chick_status='pending').order_by('-chick_date')

    context = {
        'approved_requests': approved_requests,
        'pending_requests': pending_requests,
        'search_query': search_query,
    }
    return render(request, 'pages/public_farmer_requests.html', context)