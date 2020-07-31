import pytz


def localize_timestamp(timestamp):
    """
    Takes a datetime object and converts it to stockholm time

    timestamp (datetime): The datetime object that should be converted to
    stockholm time

    Returns:

    Returns the converted datetime object (type: datetime)
    """
    stockholm_timezone = pytz.timezone("Europe/Stockholm")
    localized_timestamp = stockholm_timezone.localize(timestamp)
    return localized_timestamp
