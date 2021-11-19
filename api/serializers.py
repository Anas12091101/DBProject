from django.db import models

from cart.models import Cart, CartProduct
from product.models import Category, Product, imgSrc, testclass
from django.contrib.auth.models import User
from User.models import Profile

from rest_framework import serializers

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=imgSrc
        fields='__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model=testclass
        fields=['img']

class ProductSerializer(serializers.ModelSerializer):
    img=serializers.SerializerMethodField()
    class Meta:
        model=Product
        fields='__all__'

    def get_img(self,obj):
        # print(obj.id)
        img=obj.imgsrc_set.all()
        serializer=ImageSerializer(img,many=True)
        return serializer.data

class CartProductSerializer(serializers.ModelSerializer):
    product=serializers.SerializerMethodField()
    class Meta:
        model=CartProduct
        fields='__all__'

    def get_product(self,obj):
        product=obj.product
        ser=ProductSerializer(product,many=False)
        return ser.data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='username','is_staff','email'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'

class CartSerializer(serializers.ModelSerializer):
    cartproduct=serializers.SerializerMethodField()
    
    class Meta:
        model=Cart
        fields='__all__'

    def get_cartproduct(self,obj):
        cartproduct=obj.cartproduct_set.all()
        serializer=CartProductSerializer(cartproduct,many=True)
        return serializer.data
