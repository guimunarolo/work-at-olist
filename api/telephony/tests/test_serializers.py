from django.test import TestCase

from telephony.models import CallEvent
from telephony.serializers import CallEventSerializer
from telephony.tests.factories import CallEventFactory


class CallEventSerializerTestCase(TestCase):

    def test_validate_call_id(self):
        # test is required
        data = {
            'type': CallEvent.TYPE_END,
        }
        serializer = CallEventSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('call_id', serializer.errors)

        # test with NULL value
        data = {
            'type': CallEvent.TYPE_END,
            'call_id': None,
        }
        serializer = CallEventSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('call_id', serializer.errors)

        # test without an integer value
        data = {
            'type': CallEvent.TYPE_END,
            'call_id': 'abc',
        }
        serializer = CallEventSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('call_id', serializer.errors)

        # test with an end record already taken
        call_start = CallEventFactory.create(event_type=CallEvent.TYPE_START)
        call_end = CallEventFactory.create(call_id=call_start.call_id,
                                           event_type=CallEvent.TYPE_END)
        data = {
            'type': CallEvent.TYPE_END,
            'call_id': call_start.call_id,
        }
        serializer = CallEventSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('call_id', serializer.errors)

    def test_validate_timestamp(self):
        # test invalid timestamp
        data = {
            'type': CallEvent.TYPE_START,
            'timestamp': '3424234234234234',
        }
        serializer = CallEventSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('timestamp', serializer.errors)

    def test_validate_phone_numbers(self):
        # test invalid source
        data = {
            'type': CallEvent.TYPE_START,
            'source': '231231239',
        }
        serializer = CallEventSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('source', serializer.errors)

        # test invalid destination
        data = {
            'type': CallEvent.TYPE_START,
            'destination': '2312312390900090808',
        }
        serializer = CallEventSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('destination', serializer.errors)

        # test start call record without source
        data = {
            'type': CallEvent.TYPE_START,
            'destination': '(11) 99888-4875',
        }
        serializer = CallEventSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('source', serializer.errors)

        # test start call record without destination
        data = {
            'type': CallEvent.TYPE_START,
            'source': '(11) 99888-4875',
        }
        serializer = CallEventSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('destination', serializer.errors)

        # test successful
        data = {
            'type': CallEvent.TYPE_START,
            'source': '(11) 99888-4875',
            'destination': '(11) 99888-4875',
        }
        serializer = CallEventSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_create(self):
        # test create a start call record event.
        data = {
            'type': CallEvent.TYPE_START,
            'source': '(11) 99888-4875',
            'destination': '(11) 99888-4875',
        }
        serializer = CallEventSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        call_obj = serializer.save()
        self.assertTrue(CallEvent.started.count() is 1)

        # test create the end event for the last started call.
        data = {
            'type': CallEvent.TYPE_END,
            'call_id': call_obj.call_id,
        }
        serializer = CallEventSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertTrue(CallEvent.ended.count() is 1)
