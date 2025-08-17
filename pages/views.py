from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from .forms import SignupForm, StockForm, ChickrequestForm, FarmerRegistrationForm, FeedstockForm
from .models import Stock, Chickrequest, Farmer, Feedstock, Userprofile
from django.core.mail import send_mail 
from .models import Userprofile, FarmerMessage
from .models import ChickType


# -----------------------------
# AUTHENTICATION
# -----------------------------
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, "auth/signup.html", {"form": form})


def loginpage(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)

            # Redirect based on role
            if user.user_type == "manager":
                return redirect("manager_dashboard")
            elif user.user_type == "sales_agent":
                return redirect("sales_agent_dashboard")
            elif user.user_type == "farmer":
                return redirect("farmer_dashboard")
            else:
                return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, "pages/login.html", {"form": form})


def logout(request):
    auth_logout(request)
    return redirect('farmer_dashboard')


# -----------------------------
# LANDING PAGE
# -----------------------------
def landing_page(request):
    return render(request, "pages/farmer_dashboard.html")




@login_required
def manager_dashboard(request):
    # Get all chick types
    chick_types = ChickType.objects.all()

    # Prepare stock summary
    stock_summary = {}

    for chick_type in chick_types:
        # All stock records for this chick type
        stock_records = Stock.objects.filter(chick_type=chick_type).order_by('date_added')

        # Total quantity for this type
        total_quantity = stock_records.aggregate(total=Sum('quantity'))['total'] or 0

        stock_summary[chick_type.name] = {
            'total_quantity': total_quantity,
            'records': stock_records
        }

    # Feed stock
    feed_stock = Feedstock.objects.aggregate(total=Sum('feed_quantity'))['total'] or 0

    # Requests
    pending_requests = Chickrequest.objects.filter(chick_status='pending')
    approved_requests = Chickrequest.objects.filter(chick_status='approved')
    requests = Chickrequest.objects.all()

    context = {
        'stock_summary': stock_summary,
        'feed_stock': feed_stock,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'requests': requests,
    }

    return render(request, 'pages/manager_dashboard.html', context)



@login_required
def sales_agent_dashboard(request):
    requests = Chickrequest.objects.filter(sales_agent=request.user).order_by("-chick_date")
    context = {
        "requests": requests,
        "total_requests": requests.count(),
        "approved_count": requests.filter(chick_status="approved").count(),
        "pending_count": requests.filter(chick_status="pending").count(),
    }
    return render(request, "pages/sales_agent_dashboard.html", context)

def farmer_dashboard(request):
    query = request.GET.get("q")
    chick_requests = Chickrequest.objects.all()

    # If search is used
    if query:
        chick_requests = chick_requests.filter(
            Q(farmer_name__farmer_name__icontains=query)
        )

    context = {
        "chick_requests": chick_requests,
        "query": query,
    }
    return render(request, "pages/farmer_dashboard.html", context)

def contact_sales(request):
    sales_reps = Userprofile.objects.filter(user_type="sales_agent")

    if request.method == "POST":
        sales_rep_id = request.POST.get("sales_rep")
        name = request.POST.get("name")
        email = request.POST.get("email")
        message_text = request.POST.get("message")

        if not name or not message_text:
            messages.error(request, "Please provide your name and message.")
            return redirect("contact_sales")

        try:
            sales_rep = Userprofile.objects.get(id=sales_rep_id, user_type="sales_agent")
            # Save the message; store name/email inside the message
            full_message = f"From: {name}\nEmail: {email or 'N/A'}\n\nMessage:\n{message_text}"

            FarmerMessage.objects.create(
                recipient=sales_rep,
                subject=f"Message from {name}",
                message=full_message
            )
            messages.success(request, "Message sent successfully.")
            return redirect("contact_sales")
        except Userprofile.DoesNotExist:
            messages.error(request, "Selected sales rep does not exist.")

    return render(request, "pages/contact_sales.html", {"sales_reps": sales_reps})

@login_required

def sales_agent_messages(request):
    # Only sales agents can view their messages
    if request.user.user_type != "sales_agent":
        messages.error(request, "You are not authorized to view this page.")
        return redirect("home")

    messages_list = FarmerMessage.objects.filter(recipient=request.user).order_by("-created_at")
    return render(request, "pages/sales_agent_messages.html", {"messages_list": messages_list})


# -----------------------------
# FARMER CRUD
# -----------------------------
@login_required
def farmers_list(request):
    query = request.GET.get("q", "")  # Get search query
    if query:
        farmers = Farmer.objects.filter(
            Q(farmer_name__icontains=query) |
            Q(farmer_nin__icontains=query) |
            Q(farmer_type__icontains=query)
        )
    else:
        farmers = Farmer.objects.all()
    
    context = {
        "farmers": farmers,
        "query": query
    }
    return render(request, "pages/farmers_list.html", context)



@login_required
def register_farmer(request, id=None):
    farmer = get_object_or_404(Farmer, id=id) if id else None
    if request.method == "POST":
        form = FarmerRegistrationForm(request.POST, instance=farmer)
        if form.is_valid():
            form.save()
            messages.success(request, "Farmer saved successfully")
            return redirect("farmers_list")
    else:
        form = FarmerRegistrationForm(instance=farmer)
    return render(request, "pages/register_farmer.html", {"form": form})


@login_required
def delete_farmer(request, id):
    farmer = get_object_or_404(Farmer, id=id)
    farmer.delete()
    messages.success(request, "Farmer deleted successfully")
    return redirect("farmers_list")




# -----------------------------
# CHICK REQUESTS
# -----------------------------
@login_required
def record_request(request, id=None):
    if id:
        chick_request = get_object_or_404(Chickrequest, pk=id)
        form = ChickrequestForm(request.POST or None, instance=chick_request)
        if request.method == "POST" and form.is_valid():
            chick_req = form.save(commit=False)
            chick_req.sales_agent = request.user
            chick_req.save()
            messages.success(request, "Request updated successfully.")
            return redirect("record_request_list")
    else:
        form = ChickrequestForm(request.POST or None)  # no hidden farmer
        if request.method == "POST" and form.is_valid():
            chick_req = form.save(commit=False)
            chick_req.sales_agent = request.user
            chick_req.save()
            messages.success(request, "Chick request created successfully.")
            return redirect("record_request_list")

    requests = Chickrequest.objects.filter(sales_agent=request.user).order_by("-chick_date")
    context = {
        "form": form,
        "requests": requests,
    }
    return render(request, "pages/record_request.html", context)



@login_required
def my_requests(request):
    # Show chick requests for the logged-in farmer
    chick_requests = Chickrequest.objects.filter(farmer_name__user=request.user)

    # Optional search
    query = request.GET.get("q")
    if query:
        chick_requests = chick_requests.filter(
            farmer_name__farmer_name__icontains=query
        )

    # Handle messages (farmer sending message to sales agent)
    if request.method == "POST":
        req_id = request.POST.get("request_id")
        message_text = request.POST.get("message")
        chick_req = Chickrequest.objects.filter(id=req_id).first()
        if chick_req:
            sales_agent_username = (
                chick_req.sales_agent.username if chick_req.sales_agent else "N/A"
            )
            print(f"Message to {sales_agent_username}: {message_text}")
            messages.success(request, "Your message has been sent to the sales agent!")

    return render(request, "pages/all_request.html", {
        "chick_requests": chick_requests
    })


# -----------------------------
# FIXED APPROVE REQUEST VIEW
# -----------------------------

@login_required
def approve_request(request, id):
    FEED_BAGS_PER_REQUEST = 2

    chick_request = get_object_or_404(Chickrequest, pk=id)

    if chick_request.chick_status == "approved":
        messages.info(request, "This request is already approved.")
        return redirect("manager_dashboard")

    # ----- Deduct chicks -----
    stock_items = Stock.objects.filter(chick_type=chick_request.chick_type).order_by('date_added')
    remaining_chicks = chick_request.chick_quantity
    for stock in stock_items:
        if remaining_chicks <= 0:
            break
        if stock.quantity >= remaining_chicks:
            stock.quantity -= remaining_chicks
            stock.save(update_fields=['quantity'])
            remaining_chicks = 0
        else:
            remaining_chicks -= stock.quantity
            stock.quantity = 0
            stock.save(update_fields=['quantity'])

    if remaining_chicks > 0:
        messages.error(request, f"Not enough chicks in stock. Missing {remaining_chicks}.")
        return redirect("manager_dashboard")

    # ----- Deduct feed if needed -----
    if chick_request.feed_needed == "yes":
        feed_items = Feedstock.objects.filter(chick_type=chick_request.chick_type).order_by('date_added')
        remaining_feed = FEED_BAGS_PER_REQUEST
        for feed in feed_items:
            if remaining_feed <= 0:
                break
            if feed.feed_quantity >= remaining_feed:
                feed.feed_quantity -= remaining_feed
                feed.save(update_fields=['feed_quantity'])
                remaining_feed = 0
            else:
                remaining_feed -= feed.feed_quantity
                feed.feed_quantity = 0
                feed.save(update_fields=['feed_quantity'])

        if remaining_feed > 0:
            messages.warning(request, f"Approved chicks but not enough feed stock. Missing {remaining_feed} feed bag(s).")

    # ----- Approve request -----
    chick_request.chick_status = "approved"
    chick_request.save(update_fields=['chick_status'])  # bypass model clean

    messages.success(request, f"Request approved successfully. {chick_request.chick_quantity} chicks deducted from stock.")
    if chick_request.feed_needed == "yes" and remaining_feed == 0:
        messages.success(request, f"Feed stock reduced by {FEED_BAGS_PER_REQUEST} bag(s).")

    return redirect("manager_dashboard")


@login_required
def reject_request(request, id):
    chick_req = get_object_or_404(Chickrequest, id=id)
    chick_req.chick_status = "rejected"
    chick_req.save()
    messages.success(request, "Request rejected successfully")
    return redirect("manager_dashboard")


@login_required
def delete_request(request, id):
    chick_req = get_object_or_404(Chickrequest, id=id)
    chick_req.delete()
    messages.success(request, "Request deleted successfully")
    return redirect("record_request_list")


@login_required
def approved_sales(request):
    approved_requests = Chickrequest.objects.filter(chick_status='approved').order_by('-chick_date')
    total_quantity = approved_requests.aggregate(total=Sum('chick_quantity'))['total'] or 0
    farmers_with_chicks = approved_requests.values_list('farmer_name__farmer_name', flat=True).distinct()

    context = {
        'approved_requests': approved_requests,
        'total_quantity': total_quantity,
        'farmers_with_chicks': farmers_with_chicks,
    }
    return render(request, 'pages/approved_sales.html', context)

@login_required
def update_delivery_status(request, id):
    chick_request = get_object_or_404(Chickrequest, id=id)

    # Only the assigned sales agent can update delivery status
    if request.user != chick_request.sales_agent:
        return redirect('approved_sales')

    if request.method == 'POST':
        status = request.POST.get('chick_delivered')
        if status in ['yes', 'no']:
            chick_request.chick_delivered = status
            chick_request.save()
            messages.success(request, "Delivery status updated successfully.")

    return redirect('delivered')  # <-- redirected to delivered page



# -----------------------------
# STOCK VIEWS
# -----------------------------
@login_required
def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, "pages/stock_list.html", {"stocks": stocks})

@login_required
def stock_add(request):
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.registered_by = request.user  # auto-assign manager
            stock.save()
            return redirect("manager_dashboard")
    else:
        form = StockForm()
    return render(request, "pages/add_stock.html", {"form": form})

@login_required
def stock_update(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    if request.method == "POST":
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.success(request, "Stock updated successfully.")
            return redirect('stock_list')
    else:
        form = StockForm(instance=stock)
    return render(request, "pages/stock_add.html", {"form": form, "update": True})


# -----------------------------
# FIXED ADD FEED STOCK VIEW
# -----------------------------
@login_required
def add_feed_stock(request):
    if request.method == "POST":
        form = FeedstockForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Feed stock added successfully.")
            return redirect('feedstock_list')
    else:
        form = FeedstockForm()
    return render(request, "pages/add_feed_stock.html", {"form": form})


@login_required
def edit_feed_stock(request, id):
    feed = get_object_or_404(Feedstock, pk=id)
    if request.method == "POST":
        form = FeedstockForm(request.POST, instance=feed)
        if form.is_valid():
            form.save()
            messages.success(request, "Feed stock updated successfully.")
            return redirect('feedstock_list')
    else:
        form = FeedstockForm(instance=feed)
    return render(request, "pages/feedstock_form.html", {"form": form, "update": True})


@login_required
def delete_feed_stock(request, id):
    feed = get_object_or_404(Feedstock, pk=id)
    if request.method == "POST":
        feed.delete()
        messages.success(request, "Feed stock deleted successfully.")
        return redirect('feedstock_list')
    return render(request, "pages/feedstock_confirm_delete.html", {"feed": feed})


@login_required
def feedstock_list(request):
    feedstocks = Feedstock.objects.all()
    return render(request, 'pages/feedstock_list.html', {'feedstocks': feedstocks})


# -----------------------------
# OTHER VIEWS
# -----------------------------
# @login_required
# def farmers_with_chicks(request):
#     farmers = Farmer.objects.filter(chickrequest__chick_status='approved').distinct()
#     return render(request, "pages/farmers_with_chicks.html", {"farmers": farmers})
@login_required
def delivered_sales(request):
    delivered_requests = Chickrequest.objects.filter(chick_delivered='yes')
    return render(request, "pages/delivered_sales.html", {"delivered_requests": delivered_requests})