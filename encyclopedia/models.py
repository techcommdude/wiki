from django.db import models

# Create your models here.
class Topics(models.Model):
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=10000)