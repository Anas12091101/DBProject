from django.db import models
from django.db.models import fields

from cart.models import Cart, CartProduct
from product.models import Category, Product, imgSrc, testclass
from django.contrib.auth.models import User
from User.models import Profile
from orders.models import Order,OrderProduct

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
        print(obj.id)
        a=obj.id
        # img=obj.imgsrc_set.all()
        img=imgSrc.objects.raw('SELECT * FROM Product_imgsrc where product_id=%s',[a])
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
    profile=serializers.SerializerMethodField()
    class Meta:
        model=User
        fields='username','is_staff','email','profile'

    def get_profile(self,obj):
        profile=obj.profile
        ser=ProfileSerializer(profile,many=False)
        return ser.data

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

class OrderProductSerializer(serializers.ModelSerializer):
    product=serializers.SerializerMethodField()
    class Meta:
        model=OrderProduct
        fields='__all__'
    def get_product(self,obj):
        product=obj.product
        ser=ProductSerializer(product,many=False)
        return ser.data

class OrderSreializer(serializers.ModelSerializer):
    orderproduct=serializers.SerializerMethodField()
    username=serializers.SerializerMethodField('get_username')
    class Meta:
        model=Order
        fields='__all__'
    def get_orderproduct(self,obj):
        orderproduct=obj.orderproduct_set.all()
        serializer=OrderProductSerializer(orderproduct,many=True)
        return serializer.data
    def get_username(self,obj):
        return obj.owner.user.username
    


