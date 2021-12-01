from django.db import models
import uuid
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=200)
    # id=models.UUIDField(default=uuid.uuid4,primary_key=True,editable=False)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=200)
    categoryId=models.ForeignKey(Category,on_delete=models.CASCADE)
    price=models.IntegerField(null=False,blank=False)
    primary_image=models.ImageField(null=True,blank=True,default=None,upload_to='images')
    description=models.TextField(null=True)
    in_stock=models.IntegerField(default=0)

    def __str__(self):
        return self.name

    
class imgSrc(models.Model):  #other images of the product
    url=models.ImageField(null=True,blank=True,default=None)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    color=models.CharField(max_length=200,null=True,blank=True)
    def __str__(self):
        return self.product.name

class testclass(models.Model):
    img=models.TextField()


