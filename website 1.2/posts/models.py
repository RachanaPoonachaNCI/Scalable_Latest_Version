from django.db import models
from authentication.models import user


# Create your models here.
class post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    subheading = models.CharField(max_length=1000)
    content = models.TextField(max_length=50000)
    image = models.ImageField(upload_to="uploads", null=True)
    updated = models.DateTimeField()
    tag = models.CharField(max_length=15)
    user = models.ForeignKey(user, on_delete=models.CASCADE)

class subscriber(models.Model):
    reader = models.ForeignKey(user, on_delete=models.CASCADE)
    author = models.ForeignKey(user, on_delete=models.CASCADE,related_name='authored_posts')
    