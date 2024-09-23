from django.test import TestCase

from tasks.forms import TaskCreationForm
from tasks.models import Position, Worker


class TaskCreationFormTest(TestCase):
    def setUp(self):
        self.position1 = Position.objects.create(name="Developer")
        self.position2 = Position.objects.create(name="Manager")
        self.position3 = Position.objects.create(name="Tester")

        self.worker1 = Worker.objects.create_user(
            username="worker1", position=self.position1)
        self.worker2 = Worker.objects.create_user(
            username="worker2", position=self.position2)
        self.worker3 = Worker.objects.create_user(
            username="worker3", position=self.position3)

    def test_form_queryset_with_two_positions(self):
        form = TaskCreationForm(positions=["Developer", "Manager"])
        queryset = form.fields["assignees"].queryset
        self.assertIn(self.worker1, queryset)
        self.assertIn(self.worker2, queryset)
        self.assertNotIn(self.worker3, queryset)

    def test_form_queryset_with_one_position(self):
        form = TaskCreationForm(positions=["Developer"])
        queryset = form.fields["assignees"].queryset
        self.assertIn(self.worker1, queryset)
        self.assertNotIn(self.worker2, queryset)
        self.assertNotIn(self.worker3, queryset)

    def test_form_queryset_with_no_positions(self):
        form = TaskCreationForm()
        queryset = form.fields["assignees"].queryset
        self.assertIn(self.worker1, queryset)
        self.assertIn(self.worker2, queryset)
        self.assertIn(self.worker3, queryset)
