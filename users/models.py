from django.db import models

# Create your models here.
class User(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=15)
    token = models.CharField(max_length=10, null=True)

    def __str__(self) -> str:
        return self.email
    
