import kronos
from datetime import datetime, time, timedelta
from adminInterface.utils.firebase_utils import Firestore
from adminInterface.utils.time_utils import localize_timestamp


@kronos.register('0 30 7,12 ? * * *')
def send_automatic_notification():
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
        print(event_dict)
