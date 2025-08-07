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
from django.contrib import admin
from django.urls import path
from pages import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('login/', views.loginpage, name='login'),
    path('', views.homepage, name='home'),
    path('manager/', views.manager_dashboard, name='manager'), 
    path('saleagent/', views.salesagent, name='salesagent'),
    path('farmer/', views.homepage, name='home'),
    path('farmer/<int:id>/edit/', views.edit_farmer, name='edit_farmer'),
    path('farmer/<int:id>/delete/', views.delete_farmer, name='delete_farmer'),
    path('farmer/<int:id>/request/', views.request_chicks, name='request_chicks'),
    path('register-farmer/<int:id>/', views.register_farmer, name='register_farmer'),



    path('my_requests/', views.my_requests, name='my_requests'),
    path('profile/', views.profile_view, name='profile'), 
    path('logout/', views.logout, name='logout'),
    path('stock/', views.stock, name='stock'),
    path('approve_requests/', views.approve_requests, name='approve_requests'),
    path('farmers_list/', views.farmers_list, name='farmers_list'),
    path('approved_sales/', views.approved_sales, name='approved_sales'),
    path('record_requests/', views.record_requests, name='record_requests'),
    path('register-farmer/', views.register_farmer, name='register_farmer'),
]

