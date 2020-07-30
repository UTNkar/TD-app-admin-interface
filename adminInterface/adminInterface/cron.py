import kronos
from datetime import datetime, time, timedelta
from adminInterface.utils.firebase_utils import Firestore


@kronos.register('0 30 7,12 ? * * *')
def send_automatic_notification():
    pass
