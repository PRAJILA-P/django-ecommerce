from django.contrib import admin

# Register your models here.

from .models import VendorRegister
from .models import Product

# Register your models here.

admin.site.register(VendorRegister)
admin.site.register(Product)