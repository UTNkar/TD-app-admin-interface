import firebase_admin
from firebase_admin import firestore
from firebase_admin import messaging
import numpy as np
import datetime
from math import ceil
from sentry_sdk import capture_exception


class Firebase():
    initialized = False

    @staticmethod
    def init():
        if not Firebase.initialized:
            firebase_admin.initialize_app()
            Firebase.initialized = True


class Firestore():
    dataBase = None

    @staticmethod
    def get_instance():
        if Firestore.dataBase is None:
            Firebase.init()
            Firestore.dataBase = firestore.client()
        return Firestore.dataBase


class CloudMessaging():

    @staticmethod
    def get_instance():
        Firebase.init()
        return messaging

    @staticmethod
    def send_notification(
        registration_tokens=[],
        title="",
        content="",
        sender=""
    ):
        """
        Sends a notification to the devices that have their registration token
        in the registration_tokens list. The notifications are sent in batches
        of 99 per batch.

        Parameters:
        registration_tokens (list): A list of strings. Contains the
        registration tokens of the devices that the notification should be
        sent to

        title (string): The title of the notification

        content (string): The content/body of the notification

        sender (string): The person/group that sent the notification

        Returns:
        list that contains:
        firebase_admin.messaging.BatchResponse if a batch was sent or
        None if a batch couldn't be sent
        """
        messaging = CloudMessaging.get_instance()
        np_tokens = np.array(registration_tokens)

        # A multicast message can only be sent to up to 100 registration
        # tokens at a time. We therefor split the user's registration tokens
        # into arrays with a maximum length of 99 just to have a safe margin
        number_of_slices = ceil(np_tokens.size / 99)
        users_chunks = np.array_split(np_tokens, number_of_slices)

        # date without 0 / month without 0
        time_now = datetime.datetime.now()
        senderDate = time_now.strftime("%-d/%-m")

        responses = []
        for users_chunk in users_chunks:
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=title,
                    body=content,
                ),
                data={
                    'title': title,
                    'body': content,
                    'sender': sender,
                    'senderDate': senderDate
                },
                tokens=users_chunk.tolist(),
            )
            try:
                response = messaging.send_multicast(message)
                responses.append(response)
            except Exception as error:
                capture_exception(error)
                responses.append(None)

        return responses
