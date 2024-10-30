from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from tasks.models import Position


class WorkerViewsTests(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Tester")
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="passwordTest123",
            first_name="Test",
            last_name="User",
            position=self.position
        )
        self.client.login(username="test_user", password="passwordTest123")

    def test_worker_get_update_profile(self):
        response = self.client.post(reverse("tasks:worker-profile"), {
            "first_name": "Updated",
            "last_name": "User",
            "position": "Tester"
        })

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "User")
        self.assertEqual(self.user.position.name, "Tester")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Profile updated successfully!")

    def test_workers_list_view(self):
        response = self.client.get(reverse("tasks:workers-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/workers_list.html")
        self.assertIn("workers_list", response.context)

    def test_select_avatar_view_get(self):
        response = self.client.get(reverse("tasks:select-avatar"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/avatar_select.html")
        self.assertIn("form", response.context)

    def test_select_avatar_view_post(self):
        avatar_url = "avatars/avatar2.png"
        response = self.client.post(reverse("tasks:select-avatar"), {
            "avatar": avatar_url
        })

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.avatar, "avatars/avatar2.png")
