from datetime import date, datetime, time

from freezegun import freeze_time

from django.test import TestCase

from telephony.models import CallEvent
from telephony.services.reports import BillReport
from telephony.tests.factories import CallEventFactory


class BillReportTestCase(TestCase):

    def setUp(self):
        self.today = date.today()
        self.subscriber = 11090999093

    def test_init(self):
        bill_report = BillReport(self.subscriber)
        self.assertEqual(bill_report.subscriber, self.subscriber)
        self.assertIsInstance(bill_report.cleaned_filters, dict)

    def test_clean_filters(self):
        bill_report = BillReport(self.subscriber)

        # test default response is previous month
        response = bill_report.clean_filters({})
        test_response = {
            'created__month': self.today.month - 1,
            'created__year': self.today.year,
        }
        self.assertEqual(response, test_response)

        # test fix wrong month
        query_params = {
            'month': 13,
        }
        response = bill_report.clean_filters(query_params)
        test_response = {
            'created__month': self.today.month - 1,
            'created__year': self.today.year,
        }
        self.assertEqual(response, test_response)

        # test fix the current month to previous
        query_params = {
            'month': self.today.month,
            'year': self.today.year,
        }
        response = bill_report.clean_filters(query_params)
        test_response = {
            'created__month': self.today.month - 1,
            'created__year': self.today.year,
        }
        self.assertEqual(response, test_response)

        # test current month is january
        with freeze_time('2000-1-1'):
            query_params = {}
            response = bill_report.clean_filters(query_params)
            test_response = {
                'created__month': 12,
                'created__year': 1999,
            }
            self.assertEqual(response, test_response)

    def test_get_queryset(self):
        # bill_report = BillReport(self.subscriber)
        # start_datetime = datetime.combine(self.today, time(20, 0, 0))
        # end_time = datetime.combine(self.today, time(20, 5, 0))

        # start_event = CallEventFactory.create(event_type=CallEvent.TYPE_START,
        #                                       created=start_datetime,
        #                                       source=self.subscriber,
        #                                       call_id=123)
        # self.assertEqual(bill_report.get_queryset().count(), 0)
        # end_event = CallEventFactory.create(event_type=CallEvent.TYPE_END,
        #                                     created=end_time,
        #                                     source=None,
        #                                     call_id=123)
        # self.assertEqual(bill_report.get_queryset().count(), 1)
        pass
