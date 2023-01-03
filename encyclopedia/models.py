from django.db import models

# Create your models here.
class Topics(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=10000)

    def __str__(self) -> str:
        return f"Title: {self.title} - body: {self.body}"