import datetime

from django.test import TestCase
from django.urls import reverse

from tasks.models import TaskType, Position, Worker, Task


class TaskTypeModelTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Testing")

    def test_str_method(self):
        self.assertEqual(str(self.task_type), "Testing")


class PositionModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Tester")

    def test_str_method(self):
        self.assertEqual(str(self.position), "Tester")


class WorkerModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.worker = Worker.objects.create(
            username="test",
            password="passwordTest123",
            position=self.position,
            avatar="avatars/avatar1.png"
        )

    def test_str_method(self):
        self.assertEqual(str(self.worker), "test")


class TaskModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Tester")
        self.task_type = TaskType.objects.create(name="Testing")
        self.assignee1 = Worker.objects.create_user(
            username="test",
            password="passwordTest123",
            position=self.position,
            avatar="avatars/avatar1.png"
        )
        self.assignee2 = Worker.objects.create_user(
            username="tester2",
            password="password123",
            position=self.position,
            avatar="avatars/tester2.png"
        )
        self.giver = Worker.objects.create(
            username="test1",
            password="passwordTest123",
            position=self.position,
            avatar="avatars/avatar1.png"
        )

        self.task = Task.objects.create(
            name="Test task",
            description="Test description",
            deadline=datetime.date(2024, 10, 10),
            is_completed=False,
            priority="High",
            task_type=self.task_type,
            giver=self.giver
        )
        self.task.assignees.set([self.assignee1, self.assignee2])

    def test_str_method(self):
        self.assertEqual(
            str(self.task),
            f"Name: {self.task.name}, deadline {self.task.deadline}"
        )

    def test_get_html_url(self):
        url = reverse("tasks:task-detail", args=[self.task.id])
        expected_html = f'<a href="{url}"> Test task </a>'
        self.assertEqual(self.task.get_html_url, expected_html)

