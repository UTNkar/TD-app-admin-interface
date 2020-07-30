import kronos
from datetime import datetime, time, timedelta
from adminInterface.utils.firebase_utils import Firestore


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
        eight_am = current_date + timedelta(hours=8)

        # Add a margin of 10 minutes around 8 just for safety
        start_limit = eight_am - timedelta(minutes=10)
        end_limit = eight_am + timedelta(minutes=10)

    else:
        return

    db = Firestore.get_instance()
    events = db.collection('event')\
        .where('release', '>=', start_limit)\
        .where('release', '<=', end_limit)\
        .stream()

    for event in events:
        event_dict = event.to_dict()


    # at 12:30
    # Get all events releasing tomorrow

    # at 7:30
    # Get all events releasing in 30 minutes
