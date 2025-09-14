from django.db import models
from django.utils.text import slugify
# Create your models here.

from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)  
    slug = models.SlugField(max_length=250, unique=True,blank=True)  
    description = models.TextField(blank=True)  
    image = models.ImageField(upload_to='category', blank=True)  

    parent = models.ForeignKey(
        'self',                
        on_delete=models.CASCADE, 
        related_name='subcategories', 
        blank=True, 
        null=True
    )

    class Meta:
        ordering = ('name',)  
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)    

    def get_url(self):
        """Return URL for this category's product listing"""
        return reverse('user:products_by_category', args=[self.slug])

    def __str__(self):
        return self.name
