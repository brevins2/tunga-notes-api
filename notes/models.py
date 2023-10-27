from django.db import models
from users.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(primary_key=True, max_length=255)

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    due_date = models.DateField()
    priority = models.CharField(max_length=20)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

