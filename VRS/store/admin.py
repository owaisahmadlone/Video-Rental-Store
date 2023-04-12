from django.contrib import admin
from django.contrib.auth.models import Group, User, Permission
from django.contrib.auth.admin import UserAdmin



# Register your models here.
from .models import *




    
class StaffAdmin(admin.ModelAdmin):
    list_display = ['name', 'email','Status','date_joined' ]
    
    



admin.site.unregister(Group)

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)

admin.site.register(PurchasedList)

admin.site.register(Staff, StaffAdmin)

