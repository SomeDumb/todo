from django.contrib import admin
from django.urls import path, include
from .views import (RegistrationView, CreateTaskView, GetTaskView, \
    DeleteTaskView, CheckTaskView, GetTaskListView, UpdateTaskView)

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('create_task', CreateTaskView.as_view()),
    path('task/<int:pk>', GetTaskView.as_view()),
    path('delete_task/<int:pk>', DeleteTaskView.as_view()),
    path('check_task/<int:pk>', CheckTaskView.as_view()),
    path('update_task/<int:pk>', UpdateTaskView.as_view()),
    path('get_list', GetTaskListView.as_view()),
]