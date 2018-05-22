from django.test import TestCase

from telephony.tests.factories import CallEventFactory
from telephony.services.call_event_data import get_new_call_id


class CallEventDataTestCase(TestCase):

    def test_get_new_call_id(self):
        self.assertEqual(get_new_call_id(), 1)

        call_event = CallEventFactory.create()
        self.assertEqual(get_new_call_id(), (call_event.call_id + 1))
