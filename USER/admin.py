from django.contrib import admin

from .models import Cart, Order, OrderItem, Register, Review

# Register your models here.

admin.site.register(Register)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)