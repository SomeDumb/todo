from django.contrib import admin

from api.models import CustomUser, ToDoList, Task

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass

class TaskInline(admin.TabularInline):
    model = Task
    fields = ['text', 'header', 'deadline', 'is_complete']

@admin.register(ToDoList)
class TodoListAdmin(admin.ModelAdmin):
    inlines = [TaskInline,]
    list_display = ['user', 'count_of_tasks']
    
    def count_of_tasks(self,obj):
        return Task.objects.filter(todo_list=obj).count()