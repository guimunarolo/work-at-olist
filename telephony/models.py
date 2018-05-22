from django.db import models
from django.utils import timezone

from .services.call_event_data import get_new_call_id


class BeginningCallEventManager(models.Manager):
    """Manager wich brings only call start events."""

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs)\
                      .filter(event_type=CallEvent.TYPE_START)


class EndingCallEventManager(models.Manager):
    """Manager wich brings only call end events."""

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs)\
                      .filter(event_type=CallEvent.TYPE_END)


class CallEvent(models.Model):
    """Model responsible to store phone calls events."""

    TYPE_END, TYPE_START = 'end', 'start'
    EVENT_TYPES = (
        (TYPE_END, 'End'),
        (TYPE_START, 'Start'),
    )

    call_id = models.PositiveIntegerField(default=get_new_call_id)
    event_type = models.CharField(max_length=5, choices=EVENT_TYPES,
                                  default=TYPE_START)
    source = models.CharField(max_length=11, null=True, blank=True)
    destination = models.CharField(max_length=11, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)

    # managers
    objects = models.Manager()
    beginnings = BeginningCallEventManager()
    endings = EndingCallEventManager()

    class Meta:
        verbose_name = 'Call Event'
        verbose_name_plural = 'Call Events'
        indexes = [
            models.Index(fields=['call_id', 'event_type']),
            models.Index(
                fields=['call_id', 'event_type', 'source', 'created']),
        ]

    def __str__(self):
        return '#{} - {} - {}'.format(self.id, self.call_id, self.event_type)

    @property
    def timestamp(self):
        return int(self.created.strftime('%s'))
