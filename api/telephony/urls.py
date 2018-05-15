from django.conf.urls import url, include

from .resources import CallEventResource

urlpatterns = [
    url(r'call-events/', CallEventResource.as_view(),
    	name='telephony_call_events_resource'),
]
