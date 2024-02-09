from django.contrib import admin
from .models import Product, CartItem, FavoriteItem, Category, ProductImage


admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(FavoriteItem)
admin.site.register(Category)
admin.site.register(ProductImage)

