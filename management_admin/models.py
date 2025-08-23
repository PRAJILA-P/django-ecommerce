from django.db import models

# Create your models here.

from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)  # Category name
    slug = models.SlugField(max_length=250, unique=True,blank=True)  # URL-friendly identifier
    description = models.TextField(blank=True)  # Optional description
    image = models.ImageField(upload_to='category', blank=True)  # Optional category image

    class Meta:
        ordering = ('name',)  # Sort by name by default
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        """Return URL for this category's product listing"""
        return reverse('shop:products_by_category', args=[self.slug])

    def __str__(self):
        return self.name
