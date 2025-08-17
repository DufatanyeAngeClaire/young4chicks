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
    # Admin
    path('admin/', admin.site.urls),

    # Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logout, name='logout'),

    # Landing / Home
    path('', views.farmer_dashboard,name='home'),

    # Dashboards
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
    path('sales-agent/', views.sales_agent_dashboard, name='sales_agent_dashboard'),
    path('farmer/', views.farmer_dashboard, name='farmer_dashboard'),

    # Farmer CRUD
    path('farmers/', views.farmers_list, name='farmers_list'),
    path('farmer/register/', views.register_farmer, name='register_farmer'),
    path('farmer/register/<int:id>/', views.register_farmer, name='register_farmer_edit'),
    path('farmer/<int:id>/delete/', views.delete_farmer, name='delete_farmer'),
    path('farmer/contact-sales/', views.contact_sales, name='contact_sales'),
path("sales/messages/", views.sales_agent_messages, name="sales_agent_messages"),



    # Chick Requests
    path('requests/all/', views.record_request, name='record_request'),
    path('request/record/', views.record_request, name='record_request_create'),
    path('request/record/<int:id>/', views.record_request, name='record_request_edit'),
    path('request/<int:id>/approve/', views.approve_request, name='approve_request'),
    path('sales/approved/', views.approved_sales, name='approved_sales'),
    path('request/<int:id>/reject/', views.reject_request, name='reject_request'),
  
    path('request/<int:id>/delete/', views.delete_request, name='delete_request'),
path('requests/', views.record_request, name='record_request_list'),

    path('sales/update-status/<int:id>/', views.update_delivery_status, name='update_delivery_status'),

 path('my_requests/', views.my_requests, name='my_requests'),
    # # # Stock Management
    path('manager/stock/', views.stock_list, name='stock_list'),
    path('manager/stock/add/', views.stock_add, name='stock_add'),
    path('manager/stock/edit/<int:stock_id>/', views.stock_add, name='stock_edit'),

    # # # Feedstock Management
    path('manager/feedstock/', views.feedstock_list, name='feedstock_list'),
    path('manager/feedstock/add/', views.add_feed_stock, name='add_feed_stock'),
    path('manager/feedstock/edit/<int:id>/', views.edit_feed_stock, name='edit_feed_stock'),
    path('manager/feedstock/delete/<int:id>/', views.delete_feed_stock, name='delete_feed_stock'),
    path("manager/delivered/", views.delivered_sales, name="delivered"),
    path("farmer/contact-sales/", views.contact_sales, name="contact_sales"),


    # Public / Farmer view requests
    # path('public/requests/', views.public_farmer_requests, name='public_requests'),
]


