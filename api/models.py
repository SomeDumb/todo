from django.db import models

from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Max

class CustomUser(AbstractUser):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    
    email = models.EmailField(db_index=True, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def get_token(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    @property
    def acess_token(self):
        return self.get_token()['access']
    
    @property
    def refresh_token(self):
        return self.get_token()['refresh']
    
    def __str__(self):
        return self.username

class ToDoList(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class Task(models.Model):
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    header = models.CharField(max_length=516)
    text = models.CharField(max_length=1048)
    deadline = models.DateTimeField()
    is_complete = models.BooleanField(default=False)