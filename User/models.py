from django.contrib.auth.models import User
from django.db import models
# from django.utils import timezone
# from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    is_verified=models.BooleanField(default=False)
    address=models.TextField(null=True)
    city=models.CharField(max_length=50,null=True)


    def __str__(self):
        return self.user.username

@receiver(post_save,sender=User)
def createprofile(sender,instance,created,**kwargs):
    if created:
        user=instance
        profile=Profile.objects.create(
            user=user
        )

