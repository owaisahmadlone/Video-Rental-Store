from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
import datetime
from django.utils import timezone



# Create your models here.



class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    password = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    

    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=200)
    rent_price=models.FloatField()
    purchase_price=models.FloatField()
    image=models.ImageField(null=True, blank=True)
    description=models.TextField(null=True, blank=True)
    rating=models.FloatField(default=0)
    director=models.CharField(max_length=200)
    genre=models.CharField(max_length=200, null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    rental_duration = models.IntegerField(default=7, null=True, blank=True)

    def __str__(self):
        return self.name



    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class PersonalList(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)



class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    purchase_type = models.BooleanField(default=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, null=True)
    timeline=models.CharField(default="6 days left",max_length=200, null=True)

    @property
    def get_total(self):
        if self.purchase_type:
            total = self.product.purchase_price * self.quantity
        else:
            total = self.product.rent_price * self.quantity
        return total

    def get_timeline(self):
        if not self.purchase_type:
            time_left = (self.date_added + datetime.timedelta(days=self.product.rental_duration)) - datetime.datetime.now(timezone.utc)
            return max(time_left.days, 0)
        else:
            return 0

    def __str__(self):
        return str(self.id)
    
class PurchasedList(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    orderitems = models.ManyToManyField(OrderItem, blank=True)
    


class Staff(models.Model):
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200, null=True)
    Status = models.CharField(default='Staff', max_length=200, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        
        
        # Create a new user instance with the same email as the staff instance
        user = User.objects.create_user(
            username=self.name,
            email=self.email,
            password=self.password,
            is_staff=True,
        )

           # Retrieve the permissions you want to set to true using their human-readable names
        edit_product = Permission.objects.get(codename='add_product' )
        delete_product = Permission.objects.get(codename='delete_product')
        view_product = Permission.objects.get(codename='view_product')
        change_product = Permission.objects.get(codename='change_product')
        view_customer = Permission.objects.get(codename='view_customer')
        view_order = Permission.objects.get(codename='view_order')
        view_purchasedlist = Permission.objects.get(codename='view_purchasedlist')
        view_orderitem = Permission.objects.get(codename='view_orderitem')

        # Add the permissions to the user_permissions attribute of the user instance
        user.user_permissions.add(edit_product, delete_product, view_product, change_product, view_customer, view_order, view_purchasedlist, view_orderitem)

        # Set the user instance as the `user` attribute of the staff instance
        self.user = user

        super().save(*args, **kwargs)

  
    
        


