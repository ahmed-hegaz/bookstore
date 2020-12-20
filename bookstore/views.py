from django.shortcuts import render, redirect, reverse
from .models import *
from .forms import OrderForm
from django.shortcuts import get_object_or_404
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.decorators import login_required
from accounts.decorators import notLoggedUsers , forAdmins
from django.contrib.auth.models import Group
from accounts.decorators import notLoggedUsers, allowedUsers, forAdmins
import requests

# Create your views here.
@login_required(login_url='login')
# @allowedUsers(allowedGroups=['admin'])
@forAdmins
def home(request):
    customers= Customer.objects.all()
    orders= Order.objects.all()
    T_orders= orders.count()
    P_orders= orders.filter(status= 'Pending').count()
    D_orders= orders.filter(status= 'Delivered').count()
    PROG_orders= orders.filter(status= 'in progress').count()
    OUT_orders= orders.filter(status= 'out of order').count()
    context= {
        'customers':customers,
         'orders':orders,
         'T_orders':T_orders,
         'P_orders':P_orders,
         'D_orders':D_orders, 
         'PROG_orders':PROG_orders,
         'OUT_orders':OUT_orders,

    }
    return render(request, 'bookstore/home.html', context)

    
@login_required(login_url='login')
@forAdmins
def books(request):
    books= Book.objects.all()
    return render(request, 'bookstore/books.html', {'books':books})

@login_required(login_url='login')
def customers(request, pk):
    customer= Customer.objects.get(id=pk)
    orders= customer.order_set.all()
    number_orders= orders.count()
    mysearch = OrderFilter(request.GET, queryset=orders)
    orders = mysearch.qs
    context= {
         'customer':customer,
         'mysearch':mysearch,
         'orders':orders,
         'number_orders':number_orders,
        }
    return render(request, 'bookstore/customers.html', context)


# def create(request): 
#     form = OrderForm()
#     if request.method == 'POST':
#        # print(request.POST)
#        form = OrderForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect('/')
#     context = {'form':form}

#     return render(request , 'bookstore/my_order_form.html', context )
# def create(request): 
#     form = OrderForm()
#     if request.method == 'POST':
#        # print(request.POST)
#        form = OrderForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect('/')
#     context = {'form':form}

   
# def customer(request,pk):
#     customer = Customer.objects.get(id=pk)
#     orders = customer.order_set.all()
#     number_orders = orders.count()

#     searchFilter = OrderFilter(request.GET , queryset=orders)
#     orders = searchFilter.qs


#     context = {'customer': customer ,'myFilter': searchFilter ,
#                'orders': orders,'number_orders': number_orders }
#     return render(request , 'bookstore/customer.html',context)
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])
def create(request, pk):
    OrderFormSet = inlineformset_factory(Customer,Order,fields=('book', 'status'),extra=8)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset = Order.objects.none(), instance=customer)
    # form = OrderForm()
    if request.method == 'POST':
       #form = OrderForm(request.POST)
       formset = OrderFormSet(request.POST , instance=customer)
       if formset.is_valid():
           formset.save()
       return redirect('/')
    else:
        form = OrderForm()
    return render(request, 'bookstore/order_form.html', {'formset':formset})
    
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])
def update(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
       form = OrderForm(request.POST, instance=order)
       if form.is_valid():
           form.save()
       return redirect('/')
    # else:
    #     form = OrderForm()
    return render(request, 'bookstore/update.html', {'form':form})

# delete view for details 
@login_required(login_url='login')
@allowedUsers(allowedGroups=['admin'])
def delete(request, pk): 
    # dictionary for initial data with  
    # field names as keys 
    # fetch the object related to passed id 
    order = Order.objects.get(id=pk) 
    if request.method =="POST": 
        # delete object 
        order.delete() 
        # after deleting redirect to  
        # home page 
        return redirect('/') 
    context ={'order':order}  
    return render(request, "bookstore/delete_form.html", context)
