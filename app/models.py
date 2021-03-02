from django.db import models

# Create your models here.
class Token(models.Model):
    id = models.AutoField(primary_key=True)
    Token = models.CharField(max_length=200)
    creationTime = models.DateTimeField(default=True)
    Status = models.CharField(max_length=200)

def __str__(self):
    return self.name    