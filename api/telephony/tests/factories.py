import datetime
import uuid

import factory

from telephony.models import CallEvent


class CallEventFactory(factory.django.DjangoModelFactory):
    event_type = CallEvent.TYPE_START
    call_id = uuid.uuid4()
    source = 11992923344
    destination = 1136365566
    created = datetime.datetime.now()

    class Meta:
        model = CallEvent
