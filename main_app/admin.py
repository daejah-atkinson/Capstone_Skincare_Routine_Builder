from django.contrib import admin
from .models import Product, Brand, Routine, Favorite

# Register your models here.
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Routine)
admin.site.register(Favorite)