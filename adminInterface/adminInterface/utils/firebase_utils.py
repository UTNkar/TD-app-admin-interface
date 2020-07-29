import firebase_admin
from firebase_admin import firestore
from firebase_admin import messaging
import numpy as np
import datetime
from math import ceil
from collections import Counter
from sentry_sdk import capture_message


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
    def _send(registration_tokens=[], title="", content="", sender=""):
        """
        Performs the sending of the notification to the devices that have
        their registration token in the registration_tokens list.
        The notifications are sent in batches of 99 per batch.

        Parameters:
        registration_tokens (list): A list of strings. Contains the
        registration tokens of the devices that the notification should be
        sent to

        title (string): The title of the notification

        content (string): The content/body of the notification

        sender (string): The person/group that sent the notification

        Returns:
        dict containing the following items:

        responses (list of firebase_admin.messaging.BatchResponse):
        Contains the responses from all batches

        failure_count (int): the number of users that the notification could
        not be sent to

        error_reasons (list of strings): Contains the error messages that the
        batches occured if something went wrong
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
        failure_count = 0
        error_reasons = []

        for users_chunk in users_chunks:
            users_chunk_list = users_chunk.tolist()
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
                tokens=users_chunk_list,
            )
            try:
                response = messaging.send_multicast(message)
                responses.append(response)
            except Exception as error:
                failure_count += len(users_chunk_list)
                error_reasons.append(str(error))

        return {
            'responses': responses,
            'failure_count': failure_count,
            'error_reasons': error_reasons
        }

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
        dict containing the following items:

        success_count (int): the number of users that the notification
        was successfully sent to

        failure_count (int): the number of users that the notification could
        not be sent to

        batches_failed (int): the number of batches that failed

        error_reasons_counted (list): A list of tuples
        (error_message, amount_of_times) that contain the error message and
        the number of times it occured
        """

        statistics = CloudMessaging._send(
            registration_tokens,
            title,
            content,
            sender
        )
        responses = statistics.get('responses', [])
        failure_count = statistics.get('failure_count', 0)
        error_reasons = statistics.get('error_reasons', [])
        batches_failed = len(error_reasons)

        success_count = 0

        for response in responses:
            success_count += response.success_count
            failure_count += response.failure_count

            if response.failure_count > 0:
                for sendResponse in response.responses:
                    if not sendResponse.success:
                        error_reasons.append(str(sendResponse.exception))

        error_reasons_counted = Counter(error_reasons).items()

        if len(error_reasons) > 0:
            message = \
                "The following errors occured when sending a notification: "
            for reason, amount_of_times in error_reasons_counted:
                message += "{0}: {1}. ".format(reason, amount_of_times)

            capture_message(message)

        return {
            'error_reasons_counted': error_reasons_counted,
            'success_count': success_count,
            'failure_count': failure_count,
            'batches_failed': batches_failed,
        }
