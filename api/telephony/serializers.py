import datetime
import re
import time

from django.utils import timezone

from rest_framework import serializers

from .models import CallEvent


def validate_phone_number(value):
    if value:
        number = re.sub('[^0-9]', '', value)
        if len(number) not in (10, 11):
            raise serializers.ValidationError('Invalid phone number')
        return number


class CallEventSerializer(serializers.Serializer):
    """Serialize a data to generate a call event record."""

    type = serializers.ChoiceField(choices=CallEvent.EVENT_TYPES)
    timestamp = serializers.IntegerField(required=False, allow_null=True)
    call_id = serializers.IntegerField(required=False, allow_null=True)
    source = serializers.CharField(required=False, allow_null=True)
    destination = serializers.CharField(required=False, allow_null=True)

    def validate_timestamp(self, value):
        try:
            datetime.datetime.fromtimestamp(int(value))\
                             .strftime('%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError):
            raise serializers.ValidationError('Field timestamp is invalid')

        return value

    def validate_source(self, value):
        return validate_phone_number(value)

    def validate_destination(self, value):
        return validate_phone_number(value)

    def validate_end_type(self, data):
        """End call event records logic."""
        call_id = data.get('call_id')

        if not call_id:
            raise serializers.ValidationError({
                'call_id': 'Field call_id is required',
            })

        query_condition = CallEvent.endings.filter(call_id=call_id).exists()
        if query_condition:
            raise serializers.ValidationError({
                'call_id': 'This call is already ended',
            })

        # remove unnecessary data for end call event
        data.update({'source': None, 'destination': None})

        return data

    def validate_start_type(self, data):
        """Start call event records logic."""
        call_id = data.get('call_id')

        if not data.get('source'):
            raise serializers.ValidationError({
                'source': 'Field source is required',
            })

        if not data.get('destination'):
            raise serializers.ValidationError({
                'destination': 'Field destination is required',
            })

        query_condition = CallEvent.beginnings.filter(call_id=call_id).exists()
        if query_condition:
            raise serializers.ValidationError({
                'call_id': 'This call is already started',
            })

        return data

    def validate(self, data):
        event_type = data.get('type')

        if event_type == CallEvent.TYPE_END:
            data = self.validate_end_type(data)
        elif event_type == CallEvent.TYPE_START:
            data = self.validate_start_type(data)

        return data

    def create(self, cleaned_data):
        """Create a call event record and return the object."""
        timestamp = cleaned_data.get('timestamp')
        call_id = cleaned_data.get('call_id')
        creation_data = {
            'event_type': cleaned_data.get('type'),
            'source': cleaned_data.get('source'),
            'destination': cleaned_data.get('destination'),
        }

        if timestamp:
            creation_data.update({
                'created': datetime.datetime.fromtimestamp(timestamp)})

        if call_id:
            creation_data.update({'call_id': call_id})

        call_event = CallEvent(**creation_data)
        call_event.save()

        return call_event

    def to_representation(self, instance):
        """Override the instance representation to return on Resource."""
        return {
            'type': instance.event_type,
            'timestamp': instance.timestamp,
            'call_id': instance.call_id,
            'source': instance.source,
            'destination': instance.destination,
        }
