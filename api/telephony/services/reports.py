from datetime import time, date, datetime, timedelta

from django.db.models import OuterRef, Subquery

from telephony.models import CallEvent


class BillReport:
    # fixed charges to pay the connection
    STANDING_CHARGE = 0.36

    # rules for standard tariff (between 6h00 and 22h00)
    STANDARD_PRICE = 0.9 
    STANDARD_START_TIME = time(6, 0, 0)
    STANDARD_END_TIME = time(22, 0, 0)

    # rules for reduced tariff (between 22h00 and 6h00)
    REDUCED_PRICE = 0.0

    def __init__(self, subscriber, query_params={}, *arg, **kwargs):
        self.subscriber = subscriber
        self.cleaned_filters = self.clean_filters(query_params)
    
    def clean_filters(self, query_params):
        '''
        Returns month and year filters.
        Month needs to be a closed month, in other words it will get the
        previous month or lesser.
        '''
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
            'created__month': month,
            'created__year': year,
        }

    def get_queryset(self):
        '''
        Returns a queryset with ended call events with start created field
        annotated.
        '''
        end_query = CallEvent.ended.filter(call_id=OuterRef('call_id'))\
                                   .order_by('-created')\
                                   .values('created')[:1]
        queryset = CallEvent.started.annotate(ended=Subquery(end_query))\
                                    .filter(source=self.subscriber,
                                            ended__isnull=False,
                                            **self.cleaned_filters)
        return queryset

    def format_obj(self, obj):
        return {
            'destination': obj.destination,
            'start_date': obj.created.date(),
            'start_time': obj.created.time(),
            'duration': 0,
            'price': 0.0
        }

    def make_report(self):
        queryset = self.get_queryset()
        return {
            'count': queryset.count(),
            'filters': self.cleaned_filters,
            'objects': [self.format_obj(obj) for obj in queryset.iterator()],
        }


















