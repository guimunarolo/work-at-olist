from django.db import models
from django.utils import timezone

from .services.call_event_data import get_new_call_id


class StartedCallEventManager(models.Manager):
    '''
    Manager wich brings only call start event.
    '''
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs)\
                      .filter(event_type=CallEvent.TYPE_START)


class EndedCallEventManager(models.Manager):
    '''
    Manager wich brings only call end event.
    '''
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs)\
                      .filter(event_type=CallEvent.TYPE_END)


class CallEvent(models.Model):
    '''
    Model responsible to store phone calls events.
    '''

    TYPE_END, TYPE_START = 'en', 'st'
    EVENT_TYPES = (
        (TYPE_END, 'Ended'),
        (TYPE_START, 'Started'),
    )

    event_type = models.CharField(max_length=2, choices=EVENT_TYPES,
                                  db_index=True, default=TYPE_START)
    call_id = models.PositiveIntegerField(default=get_new_call_id,
                                          db_index=True)
    source = models.CharField(max_length=11, null=True, blank=True)
    destination = models.CharField(max_length=11, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)

    # managers
    started = StartedCallEventManager()
    ended = EndedCallEventManager()
    objects = models.Manager()

    class Meta:
        verbose_name = 'Call Event'
        verbose_name_plural = 'Call Events'

    def __str__(self):
        return '#{} - {} - {}'.format(self.id, self.call_id, self.event_type)

    @property
    def timestamp(self):
        return int(self.created.strftime('%s'))
