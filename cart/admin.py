from django.contrib import admin

from cart.models import Cart, CartProduct

# # Register your models here.
admin.site.register(Cart)
admin.site.register(CartProduct)