from django import forms
from VENDOR.models import Product
from .models import Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'   # or select specific fields like ['name', 'price', 'description', 'image']



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "slug", "description", "image", "parent"]
