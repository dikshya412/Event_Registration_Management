from datetime import time, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Event
class EventModelTest(TestCase):

    def setUp(self):
        self.organizer = User.objects.create_user(
            username='organizer',
            password='test-password-123'
        )

    def test_event_status_is_upcoming(self):
        tomorrow = timezone.localdate() + timedelta(days=1)

        event = Event.objects.create(
            title='Django Testing Workshop',
            description='Learn automated testing',
            date=tomorrow,
            time=time(10, 0),
            end_time=time(12, 0),
            venue='Computer Lab',
            organizer=self.organizer
        )

        self.assertEqual(event.status, 'Upcoming')
        