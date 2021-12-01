from django.db import models
from User.models import Profile
# Create your models here.
class Message(models.Model):
    name=models.ForeignKey(Profile,on_delete=models.CASCADE)
    subject=models.CharField(max_length=200)
    message=models.TextField(null=False)
    featured=models.BooleanField(default=False)

    def __str__(self):
        return self.name