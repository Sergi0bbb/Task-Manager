from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from tasks.models import Worker, TaskType, Position
from tasks.utils import Calendar
from datetime import date


class CalendarViewTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.user = Worker.objects.create_user(
            username="test",
            password="passwordTest123",
            position=self.position
        )
        self.task_type = TaskType.objects.create(name="Development")
        self.client.login(username="test", password="passwordTest123")

    def test_calendar_view_for_current_month(self):
        response = self.client.get(reverse("tasks:calendar"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/calendar.html")

        today = timezone.now().date()
        cal = Calendar(today.year, today.month)
        expected_html = cal.formatmonth(user=self.user, withyear=True)
        self.assertIn("calendar", response.context)
        self.assertInHTML(expected_html, str(response.context["calendar"]))

    def test_calendar_view_for_specific_month_and_year(self):
        response = self.client.get(
            reverse("tasks:calendar"),
            {"month": 7, "year": 2024}
        )

        self.assertEqual(response.status_code, 200)
        cal = Calendar(2024, 7)
        expected_html = cal.formatmonth(user=self.user, withyear=True)
        self.assertIn("calendar", response.context)
        self.assertInHTML(expected_html, str(response.context["calendar"]))

    def test_prev_and_next_month_links(self):
        today = date.today()
        response = self.client.get(reverse("tasks:calendar"))

        next_month = today.replace(day=28) + timezone.timedelta(days=4)
        next_month = next_month.replace(day=1)
        prev_month = today.replace(day=1) - timezone.timedelta(days=1)
        prev_month = prev_month.replace(day=1)

        self.assertEqual(
            response.context["prev_month"],
            f'month={prev_month.month}&year={prev_month.year}'
        )
        self.assertEqual(
            response.context["next_month"],
            f'month={next_month.month}&year={next_month.year}'
        )
