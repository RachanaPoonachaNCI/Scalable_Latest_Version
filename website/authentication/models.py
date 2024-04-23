from django.db import models


# Create your models here.
class user(models.Model):
    email = models.EmailField(primary_key=True)
    name = models.CharField(max_length=100)
