import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tasks.models import Task, TaskType, Position


class TaskViewsTests(TestCase):
    def setUp(self):
        self.pm_position = Position.objects.create(name="Project Manager")
        self.dev_position = Position.objects.create(name="Developer")

        self.pm_user = get_user_model().objects.create_user(
            username="pm_user",
            password="passwordTest123",
            position=self.pm_position
        )
        self.dev_user = get_user_model().objects.create_user(
            username="dev_user",
            password="passwordTest123",
            position=self.dev_position
        )

        self.client.login(username="pm_user", password="passwordTest123")
        self.task_type = TaskType.objects.create(name="Development")

        self.task = Task.objects.create(
            name="Task 1",
            description="First task",
            deadline=datetime.date(2024, 10, 10),
            is_completed=False,
            priority="H",
            task_type=self.task_type,
            giver=self.pm_user
        )

    def test_create_task_get(self):
        response = self.client.get(reverse("tasks:task-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_create.html")
        self.assertIn("form", response.context)

    def test_complete_task(self):
        self.assertFalse(self.task.is_completed)
        response = self.client.get(
            reverse("tasks:complete-task", args=[self.task.pk])
        )
        self.task.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.task.is_completed)

    def test_task_detail_view(self):
        response = self.client.get(
            reverse("tasks:task-detail", args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_detail.html")
        self.assertEqual(response.context["task"], self.task)

    def test_task_update_view_get(self):
        response = self.client.get(
            reverse("tasks:task-update", args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/task_update.html")
        self.assertIn("form", response.context)

    def test_task_update_view_post(self):
        updated_data = {
            "name": "Updated Task",
            "description": "Updated description",
            "deadline": "2024-10-15",
            "priority": "M",
            "task_type": self.task_type.id,
            "assignees": [self.dev_user.id],
        }
        response = self.client.post(
            reverse("tasks:task-update", args=[self.task.pk]),
            data=updated_data
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated Task")
        self.assertEqual(self.task.description, "Updated description")

    def test_task_delete_view(self):
        response = self.client.post(
            reverse("tasks:task-delete", args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
