"""CallEvent data logics."""


def get_new_call_id():
    """
    Return a new call_id based on the last registered CallEvent.

    If there is no CallEvent on base, returns 1.
    """
    from telephony.models import CallEvent

    try:
        last_call_event = CallEvent.objects.only('call_id').latest('call_id')
    except CallEvent.DoesNotExist:
        return 1

    return last_call_event.call_id + 1
