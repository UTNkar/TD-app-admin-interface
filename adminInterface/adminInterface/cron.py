import kronos
from datetime import datetime, time, timedelta
from adminInterface.utils.firebase_utils import Firestore, CloudMessaging
from adminInterface.utils.time_utils import localize_timestamp
from pytz import timezone


@kronos.register('30 7,12 * * *')  # Everyday at 7:30 and 12:30
def send_automatic_notification():
    """
    Finds all events that occur tomorrow if the current time is between
    12:00-13:00 or within 20-40 minutes if the time is 7:30 and sends a
    notification to all users that can attend the event.
    """
    current_time = datetime.now()
    current_date = datetime.today()
    current_hour = current_time.hour

    events = None
    start_limit = current_time
    end_limit = current_time

    if current_hour == 12:
        tomorrow_date = current_date + timedelta(days=1)

        start_limit = datetime.combine(tomorrow_date, time.min)
        end_limit = datetime.combine(tomorrow_date, time.max)

    elif current_hour == 7:
        eight_am = datetime.combine(current_date, time(hour=8))

        # Add a margin of 10 minutes around 8 just for safety
        start_limit = eight_am - timedelta(minutes=10)
        end_limit = eight_am + timedelta(minutes=10)

    else:
        return

    start_limit = localize_timestamp(start_limit)
    end_limit = localize_timestamp(end_limit)

    db = Firestore.get_instance()
    events = db.collection('event')\
        .where('release', '>=', start_limit)\
        .where('release', '<=', end_limit)\
        .stream()

    for event in events:
        event_dict = event.to_dict()
        attending_classes = event_dict.get("who")

        registration_tokens = Firestore\
            .get_user_registration_tokens_by_classes(attending_classes)

        content = ""
        title = ""
        sender = "Rekå"

        if current_hour == 12:
            release = event_dict.get("release")
            release_stockholm_time = release.astimezone(
                timezone("Europe/Stockholm")
            )
            release_time = release_stockholm_time.strftime("%-H:%M")

            content = (
                "Imorgon klockan {0} släpps biljetterna till {1}. "
                "Glöm inte att reservera "
                "din biljett här i appen!"
            ).format(release_time, event_dict.get("name"))

            title = (
                "Biljettsläpp för {0} öppnar imorgon"
            ).format(event_dict.get("name"))

        elif current_hour == 7:
            content = (
                "Om 30 minuter släpps biljetterna till {0}. "
                "Glöm inte att reservera din biljett här i appen!"
            ).format(event_dict.get("name"))

            title = (
                "Biljettsläpp för {0} öppnar om 30 min"
            ).format(event_dict.get("name"))

        else:
            raise ValueError((
                "Could not set a title and content "
                "for automatic reminder notification"
            ))

        CloudMessaging.send_notification(
            registration_tokens,
            title,
            content,
            sender
        )
