from django.db import models

# Create your models here.


class documents(models.Model):
    first  = models.CharField(max_length=100)
    last  = models.CharField(max_length=100)
    birthday = models.DateField(max_length=100)
    email = models.EmailField()
    phonenumber = models.IntegerField()
    image =models.ImageField()


