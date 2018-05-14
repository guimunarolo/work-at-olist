from django.test import TestCase

from telephony.models import CallEvent
from telephony.tests.factories import CallEventFactory


class CallEventFactoryTestCase(TestCase):

    def test_str(self):
        call = CallEventFactory.create()
        self.assertEqual(
            str(call), '#{} - {} - {}'.format(call.id, call.call_id,
                                              call.event_type))
