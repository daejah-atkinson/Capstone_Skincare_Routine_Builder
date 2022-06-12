from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):

    name = models.CharField(max_length=100)
    about = models.TextField(max_length=500)
    morning_application = models.BooleanField(default=True)
    evening_application = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Brand(models.Model):

    brand = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    img = models.CharField(max_length=550)
    link = models.CharField(max_length=750)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="brands")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.brand
    
    class Meta:
        ordering = ['brand']

class Routine(models.Model):
    name = models.CharField(max_length=150)
    brands = models.ManyToManyField(Brand)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

class Favorite(models.Model):
    name = models.CharField(max_length=150, default='Favorites')
    brands = models.ManyToManyField(Brand)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

