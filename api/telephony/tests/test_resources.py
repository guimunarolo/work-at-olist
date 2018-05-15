import time

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from telephony.models import CallEvent
from telephony.tests.factories import CallEventFactory

class CallEventResoiureTests(APITestCase):

    def setUp(self):
        self.url = reverse('telephony_call_events_resource')
        self.test_data = {
            'call_id': 123,
            'type': None,
            'source': '11998884875',
            'destination': '11998884876',
            'time': int(time.time()) - 10,
        }

    def test_create_start(self):
        '''
        Test create a start call event.
        '''
        data = self.test_data.copy()
        data.update({'type': CallEvent.TYPE_START})
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CallEvent.started.count(), 1)

    def test_create_end(self):
        '''
        Test create a end call event.
        '''
        data = self.test_data.copy()
        data.update({
            'type': CallEvent.TYPE_END,
            'source': None,
            'destination': None,
        })
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CallEvent.ended.count(), 1)

    def test_create_bad_request(self):
        '''
        Test create without required field.
        '''
        data = self.test_data.copy()
        data.update({
            'call_id': None,
            'type': CallEvent.TYPE_END,
            'source': None,
            'destination': None,
        })
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_not_allowed_methods(self):
        '''
        Test get, put, patch.
        '''
        response = self.client.get(self.url, {}, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(self.url, {}, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(self.url, {}, format='json')
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)
