from django.db import models
from User.models import Profile
from product.models import Product
# Create your models here.
class Order(models.Model):
    owner=models.ForeignKey(Profile,on_delete=models.CASCADE)
    status=models.CharField(max_length=200,null=True)
    total_price=models.PositiveIntegerField(default=0,null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.owner.user.username

class OrderProduct(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0)
    # profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    Order=models.ForeignKey(Order,on_delete=models.CASCADE)
    def __str__(self):
        return self.product.name