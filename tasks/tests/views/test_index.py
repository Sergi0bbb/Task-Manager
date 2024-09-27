import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tasks.models import Position, TaskType, Task


class IndexTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Tester")
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="passwordTest123",
            position=self.position
        )
        self.client.login(username="test_user", password="passwordTest123")
        self.task_type = TaskType.objects.create(name="Testing")

        task1 = Task.objects.create(
            name="Task 1",
            description="First task",
            deadline=datetime.date(2024, 10, 10),
            is_completed=False,
            priority="H",
            task_type=self.task_type,
            giver=self.user
        )
        task1.assignees.add(self.user)

        task2 = Task.objects.create(
            name="Task 2",
            description="Second task",
            deadline=datetime.date(2024, 10, 10),
            is_completed=True,
            priority="M",
            task_type=self.task_type,
            giver=self.user
        )
        task2.assignees.add(self.user)

        task3 = Task.objects.create(
            name="Task 3",
            description="Third task",
            deadline=datetime.date(2024, 10, 10),
            is_completed=False,
            priority="L",
            task_type=self.task_type,
            giver=self.user
        )
        task3.assignees.add(self.user)

    def test_graphic_tasks_per_week(self):
        response = self.client.get(reverse("tasks:home_page"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/index.html")
        self.assertIn("tasks_per_week", response.context)
        self.assertIn("is_tasks_exist", response.context)

        self.assertEqual(response.context["num_tasks"], 3)
        self.assertEqual(response.context["num_completed_tasks"], 1)
        self.assertEqual(response.context["num_uncompleted_tasks"], 2)

        self.assertEqual(
            round(response.context["completion_percentage"], 2),
            33.33
        )
