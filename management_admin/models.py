from django.db import models
from django.utils.text import slugify
# Create your models here.

from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)  # Category name
    slug = models.SlugField(max_length=250, unique=True,blank=True)  # URL-friendly identifier
    description = models.TextField(blank=True)  # Optional description
    image = models.ImageField(upload_to='category', blank=True)  # Optional category image

    parent = models.ForeignKey(
        'self',                # references the same model
        on_delete=models.CASCADE, 
        related_name='subcategories', 
        blank=True, 
        null=True
    )

    class Meta:
        ordering = ('name',)  # Sort by name by default
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        if not self.slug:  # If slug is empty, create one from the name
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)    

    def get_url(self):
        """Return URL for this category's product listing"""
        return reverse('user:products_by_category', args=[self.slug])

    def __str__(self):
        return self.name
