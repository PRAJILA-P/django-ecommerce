from django.db import models

from django.contrib.auth.hashers import make_password



from django.urls import reverse
from management_admin.models import Category
from django.utils.text import slugify
# Create your models here.

class VendorRegister(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  
    company_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    reset_token = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        
        if not self.pk:  
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.company_name or 'No Company'})"


class Product(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True,blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Foreign key to Category (from Admin app)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    vendor = models.ForeignKey('VendorRegister',on_delete=models.CASCADE,related_name='products',help_text="Vendor who added the product")

    
    discount = models.PositiveIntegerField(default=0, help_text="Discount in percentage")

    
    image = models.ImageField(upload_to='products', blank=True)
    image2 = models.ImageField(upload_to='products', blank=True)
    image3 = models.ImageField(upload_to='products', blank=True)

    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('vendor:prodCatdetail', args=[self.category.slug, self.slug])

    @property
    def final_price(self):
        """Return price after discount."""
        if self.discount > 0:
            return self.price - (self.price * self.discount / 100)
        return self.price

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
    
        while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        self.slug = slug

    
        if self.stock is None:
            self.stock = 0
        elif isinstance(self.stock, str):
            try:
                self.stock = int(self.stock)
            except ValueError:
                self.stock = 0    

    
        self.available = self.stock > 0

        super().save(*args, **kwargs)


    # def save(self, *args, **kwargs):
    #     if not self.slug:  # generate slug only if not provided
    #         base_slug = slugify(self.name)
    #         slug = base_slug
    #         counter = 1
    #         # ensure unique slug
    #         while Product.objects.filter(slug=slug).exists():
    #             slug = f"{base_slug}-{counter}"
    #             counter += 1
    #         self.slug = slug

    #     # availability based on stock
    #     self.available = self.stock > 0

    #     super().save(*args, **kwargs)

