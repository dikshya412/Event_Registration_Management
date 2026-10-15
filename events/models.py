from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    venue = models.CharField(max_length=200)

    @property
    def status(self):
        if self.end_time is None:
            return 'Unscheduled'
        current_tz = timezone.get_current_timezone()
        now = timezone.localtime()

        start = timezone.make_aware(
            timezone.datetime.combine(self.date, self.time),
            current_tz
        )
        end = timezone.make_aware(
            timezone.datetime.combine(self.date, self.end_time),
            current_tz
        )
        if end < now:
            return 'Completed'
        elif start <= now:
            return 'Ongoing'
        return 'Upcoming'

    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='organized_events'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 


class Registration(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='registrations'
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations'
    )

    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
        models.UniqueConstraint(
            fields=['student', 'event'],
            name='unique_student_event_registration'
        )
    ]

    def __str__(self):
        return f"{self.student.username} - {self.event.title}"
