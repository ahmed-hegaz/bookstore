from django.shortcuts import render, redirect
from django.http import HttpResponse 
from .forms import CreateNewUser, CustomerForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group
from bookstore.forms import * 
from bookstore.models import *
from django.core.mail import send_mail
from django.conf import settings
import requests



# Create your views here.


@notLoggedUsers
def register_1(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    # else:
        form = CreateNewUser()
        if request.method == 'POST':
            form = CreateNewUser(request.POST)
            if form.is_valid():
                
                       recaptcha_response = request.POST.get('g-recaptcha-response')
                       data = {
                           'secret' : settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                           'response' : recaptcha_response
                       }
                       r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=data)
                       result = r.json()
                       if result['success']:
                            user= form.save()
                            username = form.cleaned_data.get('username')
                            # group= Group.objects.get(name= 'customer')
                            # user.groups.add(group)
                            messages.success(request, username + 'created successfuly !')
                            return redirect('accounts:login')
                       else:
                          messages.error(request ,  ' invalid Recaptcha please try again!')  
 
        context={'form':form}
        return render(request, 'registration/register.html', context)

@notLoggedUsers    
def login_1(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    # else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('bookstore:home')
            else:
                    messages.info(request, 'error find')
        context={}
        return render(request, 'registration/login.html', context)

def logout_1(request):
    logout(request)
    return redirect('accounts:login')
    


@login_required(login_url='login')
@allowedUsers(allowedGroups=['customer'])
def userProfile(request):
    orders= request.user.customer.order_set.all()
    T_orders= orders.count()
    P_orders= orders.filter(status= 'Pending').count()
    D_orders= orders.filter(status= 'Delivered').count()
    PROG_orders= orders.filter(status= 'in progress').count()
    OUT_orders= orders.filter(status= 'out of order').count()
    context= {
         'orders':orders,
         'T_orders':T_orders,
         'P_orders':P_orders,
         'D_orders':D_orders, 
         'PROG_orders':PROG_orders,
         'OUT_orders':OUT_orders,
    }
    return render(request, 'registration/profile.html', context)

@login_required(login_url='login')
# @allowedUsers(allowedGroups=['customer'])
def profileinfo(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST': 
         form = CustomerForm(request.POST , request.FILES, instance=customer)
         if form.is_valid():
             form.save()

    context= {'form':form}
    return render(request, 'registration/profile_info.html', context)

# def send_message(request):
#     # myinfo = Info.objects.first()

#     # if request.method == 'POST':
#     #     subject = request.POST['subject']
#     #     email = request.POST['email']
#     #     message = request.POST['message']

#         send_mail(
#             subject,
#             message,
#             settings.EMAIL_HOST_USER,
#             [email],
            
#         )

#     return render(request,'contacts:home',{})

# def send_message(request):
#     if request.method == 'POST':
#         send_mail(
#         'Subject here',
#         'Here is the message.',
#         settings.EMAIL_HOST_USER,
#         [request.POST['email']],
#         fail_silently=False,
#     )
#     return render(request,'accounts:home',{})
    