from django.test import TestCase

# Create your tests here.


from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta, time

from .models import Event, Registration


class EventModelTests(TestCase):

    def setUp(self):
        self.organizer = User.objects.create_user(
            username="organizer",
            password="test123"
        )

        self.event = Event.objects.create(
            title="Django Workshop",
            description="Learn Django testing",
            date=timezone.localdate() + timedelta(days=1),
            time=time(10, 0),
            venue="Computer Lab",
            organizer=self.organizer
        )

    def test_event_creation(self):
        self.assertEqual(self.event.title, "Django Workshop")

    def test_event_has_organizer(self):
        self.assertEqual(self.event.organizer, self.organizer)

    def test_event_string_representation(self):
        self.assertEqual(str(self.event), "Django Workshop")

    def test_event_created_at_exists(self):
        self.assertIsNotNone(self.event.created_at)


class RegistrationModelTests(TestCase):

    def setUp(self):
        self.organizer = User.objects.create_user(
            username="organizer",
            password="test123"
        )

        self.student = User.objects.create_user(
            username="student",
            password="test123"
        )

        self.event = Event.objects.create(
            title="Python Workshop",
            description="Learn Python",
            date=timezone.localdate() + timedelta(days=1),
            time=time(11, 0),
            venue="Room 101",
            organizer=self.organizer
        )

    def test_registration_creation(self):
        registration = Registration.objects.create(
            student=self.student,
            event=self.event
        )

        self.assertEqual(registration.student, self.student)
        self.assertEqual(registration.event, self.event)

    def test_registration_string_representation(self):
        registration = Registration.objects.create(
            student=self.student,
            event=self.event
        )

        self.assertEqual(
            str(registration),
            "student - Python Workshop"
        )

    def test_registration_created_at_exists(self):
        registration = Registration.objects.create(
            student=self.student,
            event=self.event
        )

        self.assertIsNotNone(registration.registered_at)


class EventViewTests(TestCase):

    def setUp(self):
        self.organizer = User.objects.create_user(
            username="organizer",
            password="test123"
        )

        self.event = Event.objects.create(
            title="Django Workshop",
            description="Learn Django testing",
            date=timezone.localdate() + timedelta(days=1),
            time=time(10, 0),
            venue="Computer Lab",
            organizer=self.organizer
        )

    def test_event_list_page(self):
        response = self.client.get(
            reverse("event_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django Workshop")

    def test_event_detail_page(self):
        response = self.client.get(
            reverse("event_detail", args=[self.event.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django Workshop")

    def test_event_create_page(self):
        response = self.client.get(
            reverse("event_create")
        )

        self.assertEqual(response.status_code, 200)

    def test_event_create(self):
        response = self.client.post(
            reverse("event_create"),
            {
                "title": "Python Training",
                "description": "Python beginner training",
                "date": (
                    timezone.localdate() + timedelta(days=2)
                ).isoformat(),
                "time": "12:00",
                "venue": "Training Hall",
                "organizer": self.organizer.id,
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Event.objects.filter(
                title="Python Training"
            ).exists()
        )

    def test_event_update_page(self):
        response = self.client.get(
            reverse("event_update", args=[self.event.id])
        )

        self.assertEqual(response.status_code, 200)

    def test_event_update(self):
        response = self.client.post(
            reverse("event_update", args=[self.event.id]),
            {
                "title": "Updated Django Workshop",
                "description": "Updated description",
                "date": (
                    timezone.localdate() + timedelta(days=3)
                ).isoformat(),
                "time": "13:00",
                "venue": "Updated Computer Lab",
                "organizer": self.organizer.id,
            }
        )

        self.assertEqual(response.status_code, 302)

        self.event.refresh_from_db()

        self.assertEqual(
            self.event.title,
            "Updated Django Workshop"
        )

    def test_event_delete_confirmation_page(self):
        response = self.client.get(
            reverse("event_delete", args=[self.event.id])
        )

        self.assertEqual(response.status_code, 200)

    def test_event_delete(self):
        response = self.client.post(
            reverse("event_delete", args=[self.event.id])
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Event.objects.filter(id=self.event.id).exists()
        )
