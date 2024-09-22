from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class TaskType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(Position, on_delete=models.PROTECT, related_name="workers")
    avatar = models.CharField(default="avatars/avatar1.png", max_length=100)

    def __str__(self):
        return f"{self.username}"


class Task(models.Model):
    PRIORITY_TYPE_CHOICES = [("L", "Low"), ("M", "Medium"), ("H", "High")]

    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField()
    priority = models.CharField(choices=PRIORITY_TYPE_CHOICES, max_length=1)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name="tasks")
    assignees = models.ManyToManyField(Worker, related_name="tasks_to_do")
    giver = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name="given_tasks")

    def __str__(self):
        return f"Name: {self.name}, deadline {self.deadline}"

    @property
    def get_html_url(self):
        url = reverse("tasks:task-detail", args=(self.id,))
        return f'<a href="{url}"> {self.name} </a>'
