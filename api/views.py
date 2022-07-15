from rest_framework import status, generics, permissions, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from .serializers import (RegistrationSerializer, \
    TaskSerializer)

from .models import Task, ToDoList

class RegistrationView(generics.CreateAPIView):
    
    """
    View for registration, required fields: username, email, password
    """
    
    serializer_class = RegistrationSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({"user": self.get_serializer(user,    context=self.get_serializer_context()).data})

class CreateTaskView(generics.CreateAPIView):
    
    """
    View for creating task, required fields: header, text, deadline 
    """
    
    permission_classes = (IsAuthenticated, )
    
    serializer_class = TaskSerializer
    
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        return Response({"task":TaskSerializer(task, context=self.get_serializer_context()).data})

class GetTaskView(APIView):
    
    """
    View for getting one task by its id
    """
    
    permission_classes = (IsAuthenticated, )
    
    serializer_class = TaskSerializer
    
    def get(self, request, pk):
        todo_list = get_object_or_404(ToDoList, user=request.user)
        task = get_object_or_404(Task, id=pk, todo_list=todo_list)
        serializer = TaskSerializer(task)

        return Response(serializer.data)

class GetTaskListView(generics.ListAPIView):
    
    """ 
    View for getting list of tasks
    """
    
    permission_classes = (IsAuthenticated, )
    
    serializer_class = TaskSerializer
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"tasks":serializer.data})
    
    def get_queryset(self):
        todo_list = get_object_or_404(ToDoList, user=self.request.user)
        tasks = Task.objects.filter(todo_list=todo_list)
        return tasks

class UpdateTaskView(generics.UpdateAPIView):
    
    """
    View for changing tasks fields
    """
    
    permission_classes = (IsAuthenticated, )
    
    serializer_class = TaskSerializer
    
    def patch(self, request, pk):
        todo_list = get_object_or_404(ToDoList, user=request.user)
        task = get_object_or_404(Task, id=pk, todo_list=todo_list)
        serializer = self.get_serializer(task, data=request.data, partial=True)

        if serializer.is_valid():
            task = serializer.save()
            return Response({"task": serializer.data})

        else:
            return Response({"message": "failed", "details": serializer.errors})
        
    def put(self, request, pk):
        todo_list = get_object_or_404(ToDoList, user=request.user)
        task = get_object_or_404(Task, id=pk, todo_list=todo_list)
        serializer = self.get_serializer(task, data=request.data, partial=False)

        if serializer.is_valid():
            task = serializer.save()
            return Response({"task": serializer.data})

        else:
            return Response({"message": "failed", "details": serializer.errors}) 
   
class DeleteTaskView(generics.DestroyAPIView):
    
    """
    View for deleting tasks by their id
    """
    
    permission_classes = (IsAuthenticated, )
    
    serializer_class = TaskSerializer
    
    def destroy(self, request, pk):
        todo_list = get_object_or_404(ToDoList, user=request.user)
        task = get_object_or_404(Task, id=pk, todo_list=todo_list)
        self.perform_destroy(task)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CheckTaskView(APIView):
    
    """
    View for setting tasks field is_complete to true or false
    """
    
    permission_classes = (IsAuthenticated, )
    
    serializer_class = TaskSerializer
    
    def patch(self, request, pk):
        todo_list = get_object_or_404(ToDoList, user=request.user)
        task = get_object_or_404(Task, id=pk, todo_list=todo_list)
        checked = (not task.is_complete)
        serializer = TaskSerializer(task, data={"is_complete":checked}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data={"task":serializer.data})