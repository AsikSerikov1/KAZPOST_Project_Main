from django.contrib import admin
from .models import Product, CartItem, FavoriteItem, Category


admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(FavoriteItem)
admin.site.register(Category)

