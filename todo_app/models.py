# todo_list/todo_app/models.py
from django.utils import timezone

from django.db import models
from django.urls import reverse
from datetime import datetime   

def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)


class ToDoList(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def get_absolute_url(self):
        return reverse("list", args=[self.id])

    def __str__(self):
        return self.title


class ToDoItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(default=datetime.now)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE)

    def url(self):
        return reverse(
            "item-update", args=[str(self.todo_list.id), str(self.id)]
        )

    def __str__(self):
        return f"{self.title}: due {self.due_date}"

    class Meta:
        ordering = ["due_date"]
