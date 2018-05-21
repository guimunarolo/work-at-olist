from datetime import time, date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from django.db.models import OuterRef, Subquery

from telephony.models import CallEvent


class BillReport:
    """
    Responsible to generate a Bill Reportself.

    Args:
        subscriber - Subscriber phone number
        query_params (opitional) - filters month and year
    """

    # fixed charges to pay the connection
    STANDING_CHARGE = 0.36

    # rules for standard tariff (between 6h00 and 22h00)
    STANDARD_CHARGE_PRICE = 0.09
    STANDARD_CHARGE_START_TIME = time(6, 0, 0)
    STANDARD_CHARGE_END_TIME = time(22, 0, 0)

    # rules for reduced tariff (between 22h00 and 6h00)
    REDUCED_PRICE = 0.0

    def __init__(self, subscriber, query_params={}, *arg, **kwargs):
        """Set initial attributes."""
        self.subscriber = subscriber
        self.cleaned_filters = self._clean_filters(query_params)

    def _clean_filters(self, query_params):
        """
        Return month and year filters.

        Month needs to be a closed month, in other words it will get the
        previous month or lesser.
        """
        today = date.today()
        default_month = today.month - 1
        default_year = today.year

        try:
            month = int(query_params.get('month'))
        except (ValueError, TypeError):
            month = default_year

        try:
            year = int(query_params.get('year'))
        except (ValueError, TypeError):
            year = today.year

        # set last month if month is invalid
        is_invalid_month = month not in range(1, 13)
        if is_invalid_month:
            month = default_month

        # set last month if it is the current month
        is_current_month = (month, year) == (today.month, today.year)
        if is_current_month:
            month = default_month

        # set december of last year if current month is january
        if not month:
            month = 12
            year -= 1

        return {
            'ended__month': month,
            'ended__year': year,
        }

    def get_queryset(self):
        """Return a queryset with completed calls."""
        end_query = CallEvent.endings.filter(call_id=OuterRef('call_id'))\
                                   .order_by('-created')\
                                   .values('created')[:1]
        queryset = CallEvent.beginnings.annotate(ended=Subquery(end_query))\
                                    .filter(source=self.subscriber,
                                            ended__isnull=False,
                                            **self.cleaned_filters)
        return queryset

    def _calc_duration(self, start, end):
        """
        Resturn a relativedelta between start/endself.

        Args:
            start - datetime
            end - datetime
        """
        return relativedelta(end, start)

    def _dates_between(self, start_date, end_date):
        """
        Generate dates between start and end.

        Args:
            start_date - date
            end_date - date
        """
        start_date = datetime.combine(start_date, time.min)
        end_date = datetime.combine(end_date, time.min)
        days_between = (end_date - start_date).days
        for x in range(0, days_between + 1):
            yield start_date + timedelta(x)

    def _calc_charge(self, call_start, call_end):
        """
        Implement the tarif logic.

        Args:
            call_start - datetime
            call_end - datetime
        """
        charges = [self.STANDING_CHARGE]

        for loop_date in self._dates_between(call_start.date(),
                                             call_end.date()):
            charge_start = datetime.combine(loop_date,
                                            self.STANDARD_CHARGE_START_TIME)
            charge_end = datetime.combine(loop_date,
                                          self.STANDARD_CHARGE_END_TIME)

            if call_start > charge_start:
                charge_start = call_start

            if call_end < charge_end:
                charge_end = call_end

            charge_minutes = int(
                (charge_end-charge_start).total_seconds() / 60)
            if charge_minutes > 0:
                charges.append(charge_minutes * self.STANDARD_CHARGE_PRICE)

        return sum(charges)

    def _format_duration(self, duration):
        hours = duration.days*24 + duration.hours
        return '{}h{}m{}s'.format(hours, duration.minutes,
                                  duration.seconds)

    def _format_charge(self, charge):
        return 'R$ {:.2f}'.format(charge).replace('.', ',')

    def _format_obj(self, obj):
        duration = self._calc_duration(obj.created, obj.ended)
        charge = self._calc_charge(obj.created, obj.ended)
        return {
            'destination': obj.destination,
            'start_date': obj.created.date(),
            'start_time': obj.created.time(),
            'duration': self._format_duration(duration),
            'price': self._format_charge(charge),
        }

    def _format_filters(self, filters):
        return {
            'month': filters.get('ended__month'),
            'year': filters.get('ended__year'),
        }

    def make_report(self):
        """Return a dict with full report response."""
        queryset = self.get_queryset()
        return {
            'count': queryset.count(),
            'filters': self._format_filters(self.cleaned_filters),
            'objects': [self._format_obj(obj) for obj in queryset.iterator()],
        }
