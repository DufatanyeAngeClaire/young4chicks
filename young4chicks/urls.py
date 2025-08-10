"""
URL configuration for young4chicks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib import admin
from pages import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.signup, name='signup'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logout, name='logout'),

    # Home & Dashboards
     path('', views.public_farmer_requests, name='landing_page'), # Landing page that routes based on user type
     path('', views.landing_page, name='landing_page'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('salesagent/', views.sales_agent_dashboard, name='sales_agent_dashboard'),
    path('salesagent/update_delivery/<int:pk>/', views.update_delivery_status, name='update_delivery_status'),
    path('farmer/', views.farmer_dashboard, name='farmer_dashboard'),


    # Farmer CRUD
    path('farmers_list/', views.farmers_list, name='farmers_list'),
    path('register-farmer/', views.register_farmer, name='register_farmer'),
    path('register-farmer/<int:id>/', views.register_farmer, name='register_farmer_edit'),
    path('farmer/<int:id>/edit/', views.edit_farmer, name='edit_farmer'),
    path('farmer/<int:id>/delete/', views.delete_farmer, name='delete_farmer'),

    # Chick Requests
    path('record_request/', views.record_request, name='record_request_create'),
    path('record_request/<int:id>/', views.record_request, name='record_request_edit'),

    path('my_requests/', views.my_requests, name='my_requests'),
    path('edit_request/<int:id>/', views.edit_request, name='edit_request'),
    path('delete_request/<int:id>/', views.delete_request, name='delete_request'),

    path('all_requests/', views.all_requests, name='all_requests'),

    path('approve_request/<int:id>/', views.approve_request, name='approve_request'),
    path('reject_request/<int:id>/', views.reject_request, name='reject_request'),

    path('chickrequest_list/', views.chickrequest_list, name='chickrequest_list'),

    # Profile & Misc
    path('profile/', views.profile_view, name='profile'),
    path('stock/', views.stock, name='stock'),
    path('approve_requests/', views.approve_requests, name='approve_requests'),
    path('approved_sales/', views.approved_sales, name='approved_sales'),

    # Stock Management
    path('manager/stock/add/', views.add_or_update_stock, name='add_stock'),
    path('manager/stock/<int:stock_id>/edit/', views.add_or_update_stock, name='edit_stock'),

    # Requests List and Send
    path('record_request/', views.record_request, name='record_request'),
    path('record_request/<int:id>/', views.record_request, name='record_request'),
    path('request/<int:request_id>/delete/', views.delete_request, name='request_delete'),
    path('request/<int:request_id>/send/', views.send_request, name='send_request'),

]

