import logging
from datetime import date

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CallEvent
from .serializers import CallEventSerializer
from .services.bill_report import BillReport


class CallEventResource(APIView):
    '''
    Resource responsible to receive call events records.
    '''
    serializer = CallEventSerializer
    logger = logging.getLogger('telephony.resources.CallEventResource')

    def http_method_not_allowed(self, request, *args, **kwargs):
        self.logger.warning('Method not allowed {}'.format(request.method))
        super().http_method_not_allowed(request, *args, **kwargs)

    def post(self, request, format=None):
        self.logger.info('Received requests with data {}'.format(request.data))

        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            self.logger.info('Serializer validated, saving')

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        self.logger.info('Serializer found error {}'.format(serializer.errors))

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BillReportResource(APIView):
    '''
    Resource responsible to respond a bill resport.
    '''

    def get(self, request, subscriber, format=None):
        query_params = self.request.query_params.copy()
        report = BillReport(subscriber, query_params=query_params)
        response = report.make_report()
        return Response(response)
