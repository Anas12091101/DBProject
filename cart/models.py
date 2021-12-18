from django.db import models
from User.models import Profile
from product.models import Product
# Create your models here.
class Cart(models.Model):
    profile=models.OneToOneField(Profile,on_delete=models.CASCADE)
    price=models.PositiveIntegerField(default=0,null=True)
#id auto generated as 1 for the first and increments afterwards 
    def __str__(self):
        return self.profile.user.username
    
class CartProduct(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    quantity=models.PositiveIntegerField(default=0)
    # profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    def __str__(self):
        return self.product.name

