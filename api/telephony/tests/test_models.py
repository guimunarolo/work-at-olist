import datetime
import time

from django.test import TestCase

from telephony.tests.factories import CallEventFactory


class CallEventFactoryTestCase(TestCase):

    def test_str(self):
        call = CallEventFactory.create()
        self.assertEqual(
            str(call), '#{} - {} - {}'.format(call.id, call.call_id,
                                              call.event_type))

    def test_call_id_default(self):
        call = CallEventFactory.create()
        call2 = CallEventFactory.create()
        self.assertEqual(call2.call_id, call.call_id + 1)

    def test_timestamp_property(self):
        current_time = time.time()
        call = CallEventFactory.create(
            created=datetime.datetime.fromtimestamp(int(current_time)))
        self.assertEqual(call.timestamp, int(current_time))
