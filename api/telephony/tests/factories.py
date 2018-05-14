import datetime
import uuid

import factory

from telephony.models import CallEvent


class CallEventFactory(factory.django.DjangoModelFactory):
    source = 11992923344
    destination = 1136365566

    class Meta:
        model = CallEvent
