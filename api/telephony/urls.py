from django.conf.urls import include, url

from .resources import BillReportResource, CallEventResource

urlpatterns = [
    url(r'^call-events/$', CallEventResource.as_view(),
        name='telephony_call_events_resource'),
    url(r'^bill-report/(?P<subscriber>[0-9]{11,12})/$',
        BillReportResource.as_view(), name='telephony_bill_report_resource'),
]
