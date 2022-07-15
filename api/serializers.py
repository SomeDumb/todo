from rest_framework import  serializers
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from .models import CustomUser, Task, ToDoList

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password':{'write_only': True},
            }
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['username'], \
            password = validated_data['password'], email = validated_data['email'])
        return user

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ('todo_list',)
        
        extra_kwargs = {
            'header': {'required': True},
            'text': {'required': True},
            'deadline' : {'required': True},
            }
        
    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        todo_list, created = ToDoList.objects.get_or_create(user=user)
        task = Task.objects.create(todo_list=todo_list, **validated_data)
        return task

