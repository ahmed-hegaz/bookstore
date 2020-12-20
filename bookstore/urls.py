"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import views
from accounts import urls


app_name= 'bookstore'

urlpatterns = [
    
    path('', views.home, name= 'home'),
    path('books/', views.books, name= 'books'),
    path('customers/<str:pk>', views.customers, name= 'customers'),
    # path('create/', views.create, name= 'create'),
    path('create/<str:pk>', views.create, name= 'create'),
    path('update/<str:pk>', views.update, name= 'update'),
    path('delete/<str:pk>', views.delete, name= 'delete'),
    # path('admin/', admin.site.urls),
]

