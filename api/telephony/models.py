import uuid
from datetime import datetime

from django.db import models


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
                                  db_index=True)
    call_id = models.UUIDField(default=uuid.uuid4, db_index=True)
    source = models.CharField(max_length=11, null=True, blank=True)
    destination = models.CharField(max_length=11, null=True, blank=True)
    created = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = 'Call Event'
        verbose_name_plural = 'Call Events'

    def __str__(self):
        return '#{} - {} - {}'.format(self.id, self.call_id, self.event_type)
