from django.http import JsonResponse
import json
import datetime
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password



def customer_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        email = request.POST.get('email', '')

        if not username:
            error_message = "Please fill the username!!!"
            return render(request, 'store/customer_signup.html', {'error_message': error_message})
        
        if not password1:
                error_message = "Please fill the password!!!"
                return render(request, 'store/customer_signup.html', {'error_message': error_message})


        if password1 != password2:
            error_message = "Passwords do not match!!!"
            return render(request, 'store/customer_signup.html',{'error_message': error_message})

        if User.objects.filter(username=username).exists():
            error_message = "Username already exists!!!"
            return render(request, 'store/customer_signup.html', {'error_message': error_message})

        user = User.objects.create_user(username=username, password=password1, email=email)
        customer = Customer.objects.create(user=user, name=username, email=email, password=password1)

        login(request, user)
        success_message = "Account created successfully!!!"
        return render(request, 'store/customer_login.html', {'success_message': success_message})
        
    return render(request, 'store/customer_signup.html')

def customer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username:
            error_message = "Please fill the username!!!"
            return render(request, 'store/customer_login.html', {'error_message': error_message})
        
        if not password:
                error_message = "Please fill the password!!!"
                return render(request, 'store/customer_login.html', {'error_message': error_message})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            error_message = "Invalid username or password!!!"
            return render(request, 'store/customer_login.html', {'error_message': error_message})

    return render(request, 'store/customer_login.html')

def staff_login(request):
     if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username:
            error_message = "Please fill the username!!!"
            return render(request, 'store/staff_login.html', {'error_message': error_message})
        
        if not password:
                error_message = "Please fill the password!!!"
                return render(request, 'store/staff_login.html', {'error_message': error_message})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/admin')
        else:
            error_message = "Invalid username or password!!!"
            return render(request, 'store/staff_login.html', {'error_message': error_message})

     return render(request, 'store/staff_login.html')

def get_products(request):
    products = Product.objects.all()
    product_list = [{'name': p.name, 'genre': p.genre} for p in products]
    return JsonResponse({'products': product_list})


def role(request):
     return render(request, 'store/role.html')

def store(request):
     if request.user.is_authenticated:
          if( request.user.is_staff == True):
               return redirect('/admin')
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items
     else:
          items = []
          order = {'get_cart_total': 0, 'get_cart_items': 0}
          cartItems = order['get_cart_items']
     products = Product.objects.all()
     personal_list = PersonalList.objects.filter(customer=customer).first()
     context = {'products': products, 'cartItems': cartItems, 'personal_list': personal_list}
     return render(request,'store/store.html', context)

def mylist(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin')

        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        personal_list = PersonalList.objects.filter(customer=customer).first()
        cartItems = order.get_cart_items
    else:
        personal_list = None
        cartItems = order.get_cart_items

    context = {'cartItems': cartItems,'personal_list': personal_list}
    return render(request, 'store/my-list.html', context)

def popular(request):
     if request.user.is_authenticated:
          if( request.user.is_staff == True):
               return redirect('/admin')
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items
          Genres =["Action", "Adventure","Comedy", "Crime", "Drama", "Fantasy","Horror","Romance", "Sci-Fi", "Thriller","Musical"]
          products = Product.objects.all()
          personal_list = PersonalList.objects.filter(customer=customer).first()
     context = {'products': products, 'cartItems': cartItems, 'Genres': Genres,'personal_list': personal_list}
     
     return render(request,'store/popular.html', context)

     

def removeFromList(request, productName):
    customer = request.user.customer
    product = Product.objects.get(name=productName)

    if product:
        personal_list, created = PersonalList.objects.get_or_create(customer=customer)
        personal_list.products.remove(product)
        return JsonResponse(True)
    else:
        return JsonResponse(True)


def addToList(request, productName):
    customer = request.user.customer
    product = Product.objects.get(name=productName)

    if product:
        personal_list, created = PersonalList.objects.get_or_create(customer=customer)
        personal_list.products.add(product)
        return JsonResponse(True)
    else:
        return JsonResponse(True)






def toggle_purchaseType(request, itemName):
    print('I am proceeding!.....')
    item = OrderItem.objects.get(name=itemName)
    print(item.name)
    try:
        item.purchase_type = not item.purchase_type
        item.save()
        data = {'purchase_type': item.purchase_type}
        print('Data:', data)
        return JsonResponse(data)

    except item.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)


def view_product(request, product_name):
    product = Product.objects.get(name=product_name)
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    cartItems = order.get_cart_items
    context = {'product': product, 'cartItems': cartItems}
    return render(request, 'store/view.html', context)


def cart(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items

     else:
          items = []
          order = {'get_cart_total': 0, 'get_cart_items': 0}
          cartItems = order['get_cart_items']

     context = {'items': items, 'order': order, 'cartItems': cartItems}
     return render(request, 'store/cart.html', context)


def checkout(request):
     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          items = order.orderitem_set.all()
          cartItems = order.get_cart_items

     else:
          items = []
          order = {'get_cart_total': 0, 'get_cart_items': 0}
          cartItems = order['get_cart_items']

     context = {'items': items, 'order': order, 'cartItems': cartItems}
     return render(request, 'store/checkout.html', context)


def updateItem(request):
     data = json.loads(request.body)
     productId = data['productId']
     action = data['action']

     print('Action:', action)
     print('productId:', productId)

     customer = request.user.customer
     product = Product.objects.get(id=productId)
     order, created = Order.objects.get_or_create(customer=customer, complete=False)

     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
     orderItem.name = product.name

     if action == 'add':
          orderItem.quantity = (orderItem.quantity + 1)
     elif action == 'remove':
          orderItem.quantity = (orderItem.quantity - 1)

     orderItem.save()

     if orderItem.quantity <= 0:
          orderItem.delete()

     return JsonResponse('item was added', safe=False)

def history(request):
     customer = request.user.customer
     rentedItems=0
     purchasedItems=0
     purchased_list, created = PurchasedList.objects.get_or_create(customer=customer)
     if request.user.is_authenticated:
          if( request.user.is_staff == True):
               return redirect('/admin')
          orders= Order.objects.filter(customer=customer, complete=True)
          order_list = list(orders)
          for order in order_list:
              purchased_items_set = order.orderitem_set.all()
              for item in purchased_items_set:
                  if item.purchase_type:
                      purchased_list.orderitems.add(item)
                      purchasedItems = purchasedItems + item.quantity
                  else:
                      rentedItems = rentedItems + item.quantity
                      purchased_list.orderitems.add(item)
     else:
          purchased_list=None
          order = {'get_cart_total': 0, 'get_cart_items': 0}
     products = Product.objects.all()
     totalItems = purchasedItems+rentedItems
     cartItems = totalItems
     context = {'products': products, 'purchasedItems': purchasedItems, 'rentedItems': rentedItems,'totalItems': totalItems, 'purchased_list': purchased_list,'cartItems': cartItems}
     return render(request,
               'store/history.html', context)



def processOrder(request):
     transaction_id = datetime.datetime.now().timestamp()
     data = json.loads(request.body)

     if request.user.is_authenticated:
          customer = request.user.customer
          order, created = Order.objects.get_or_create(customer=customer, complete=False)
          total = float(data['form']['total'])
          order.transaction_id = transaction_id

          if total == order.get_cart_total:
               order.complete = True
          order.save()

     else:
          print("User is not logged in!")

     return JsonResponse('Payment Complete!', safe=False)



