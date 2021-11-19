from django.contrib import admin
from .models import Category, Product, imgSrc, testclass
# Register your models here.
admin.site.register(Category)
# admin.site.register(testclass)
admin.site.register(Product)
admin.site.register(imgSrc)

