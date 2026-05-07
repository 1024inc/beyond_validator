from dateutil.relativedelta import relativedelta
from datetime import datetime


def utc_today(as_datetime=False):
    """Returns the date of today as a date object by default or as
    a datetime object if as_datetime=True."""
    now = utc_now()
    if as_datetime:
        return now.replace(minute=0, hour=0, second=0, microsecond=0)
    return now.date()

def utc_now():
    """Returns a datetime object being now."""
    return datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
