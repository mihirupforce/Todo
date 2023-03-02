# todo_list/todo_app/models.py
from django.db import models
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User


class ToDoList(models.Model):
    title = models.CharField(max_length=100, unique=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='todolist',on_delete=models.CASCADE,null=True,blank=True)


    def get_absolute_url(self):
        return reverse("list", args=[self.id])

    def __str__(self):
        return self.title
    


class ToDoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(default=datetime.now)
    is_completed = models.BooleanField(default=False)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)

    def url(self):
        return reverse(
            "item-update", args=[str(self.todo_list.id), str(self.id)]
        )

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["due_date"]

    
