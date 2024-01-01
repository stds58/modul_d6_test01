from django.contrib import admin
from .models import Category, Product, Material, ProductMaterial


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Material)
admin.site.register(ProductMaterial)
