from datetime import date, datetime, time, timedelta
from dateutil.relativedelta import relativedelta

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
        """Test init set attributes."""
        bill_report = BillReport(self.subscriber)
        self.assertEqual(bill_report.subscriber, self.subscriber)
        self.assertIsInstance(bill_report.cleaned_filters, dict)

    def test_clean_filters(self):
        """Test month filters logics."""
        bill_report = BillReport(self.subscriber)

        # test default response is previous month
        response = bill_report._clean_filters({})
        test_response = {
            'ended__month': self.today.month - 1,
            'ended__year': self.today.year,
        }
        self.assertEqual(response, test_response)

        # test fix wrong month
        query_params = {
            'month': 13,
        }
        response = bill_report._clean_filters(query_params)
        test_response = {
            'ended__month': self.today.month - 1,
            'ended__year': self.today.year,
        }
        self.assertEqual(response, test_response)

        # test fix the current month to previous
        query_params = {
            'month': self.today.month,
            'year': self.today.year,
        }
        response = bill_report._clean_filters(query_params)
        test_response = {
            'ended__month': self.today.month - 1,
            'ended__year': self.today.year,
        }
        self.assertEqual(response, test_response)

        # test current month is january
        with freeze_time('2000-1-1'):
            query_params = {}
            response = bill_report._clean_filters(query_params)
            test_response = {
                'ended__month': 12,
                'ended__year': 1999,
            }
            self.assertEqual(response, test_response)

    def test_get_queryset(self):
        """Test queryset logic."""
        filters = {'month': 12, 'year': 2017}
        bill_report = BillReport(self.subscriber, query_params=filters)
        start_datetime = datetime(2017, 12, 12, 15, 7, 13)
        end_time = datetime(2017, 12, 12, 15, 14, 56)

        # created only start event
        CallEventFactory.create(event_type=CallEvent.TYPE_START,
                                created=start_datetime,
                                source=self.subscriber,
                                call_id=123)
        self.assertEqual(bill_report.get_queryset().count(), 0)

        # created only end event (another call_id)
        CallEventFactory.create(event_type=CallEvent.TYPE_START,
                                created=start_datetime,
                                call_id=312)
        self.assertEqual(bill_report.get_queryset().count(), 0)

        # created the end, should work
        CallEventFactory.create(event_type=CallEvent.TYPE_END,
                                created=end_time,
                                source=None,
                                call_id=123)
        self.assertEqual(bill_report.get_queryset().count(), 1)

    def test_calc_charge(self):
        """Test tariff charge calc lofic."""
        bill_report = BillReport(self.subscriber)

        # test normal call
        start_datetime = datetime.combine(self.today, time(21, 57, 13))
        end_datetime = datetime.combine(self.today, time(22, 10, 56))
        response = bill_report._calc_charge(start_datetime, end_datetime)
        self.assertEqual(response, 0.54)

        # test between months
        start_datetime = datetime.combine(date(2018, 2, 28), time(21, 57, 13))
        end_datetime = datetime.combine(date(2018, 3, 1), time(22, 10, 56))
        response = bill_report._calc_charge(start_datetime, end_datetime)
        self.assertEqual(response, 86.94)

    def test_calc_duration(self):
        """Test return type."""
        bill_report = BillReport(self.subscriber)
        response = bill_report._calc_duration(date.today(), date.today())
        self.assertIsInstance(response, relativedelta)

    def test_dates_between(self):
        """Test generation."""
        bill_report = BillReport(self.subscriber)
        response = bill_report._dates_between(date.today(), date.today())
        self.assertEqual(len(list(response)), 1)
        for item in response:
            self.assertIsInstance(item, date)

    def test_format_duration(self):
        """Test duration formatation."""
        bill_report = BillReport(self.subscriber)
        start = datetime.now()
        end = start + timedelta(days=1, hours=1, minutes=2, seconds=3)
        response = bill_report._format_duration(relativedelta(end, start))
        self.assertEqual(response, '25h2m3s')

    def test_format_charge(self):
        """Test charge formatation."""
        bill_report = BillReport(self.subscriber)
        response = bill_report._format_charge(122.34)
        self.assertEqual(response, 'R$ 122,34')

    def test_format_obj(self):
        """Test object formatation."""
        filters = {'month': 12, 'year': 2017}
        start_datetime = datetime(2017, 12, 12, 15, 7, 13)
        end_time = datetime(2017, 12, 12, 15, 14, 56)
        CallEventFactory.create(event_type=CallEvent.TYPE_START,
                                created=start_datetime,
                                source=self.subscriber,
                                call_id=123)
        CallEventFactory.create(event_type=CallEvent.TYPE_END,
                                created=end_time,
                                source=None,
                                call_id=123)
        bill_report = BillReport(self.subscriber, query_params=filters)
        response = bill_report._format_obj(bill_report.get_queryset()[0])
        self.assertIsInstance(response, dict)
        conditions = [
            'destination' in response,
            'start_date' in response,
            'start_time' in response,
            'duration' in response,
            'price' in response,
        ]
        self.assertTrue(all(conditions))

    def test_format_filters(self):
        """Test filters formatation."""
        filters = {'month': 12, 'year': 2017}
        bill_report = BillReport(self.subscriber, query_params=filters)
        response = bill_report._format_filters(bill_report.cleaned_filters)
        self.assertEqual(response, filters)

    def test_make_report(self):
        """Test make report formatation."""
        bill_report = BillReport(self.subscriber)
        response = bill_report.make_report()
        self.assertIsInstance(response, dict)
        conditions = [
            'count' in response,
            'filters' in response,
            'objects' in response,
        ]
        self.assertTrue(all(conditions))
