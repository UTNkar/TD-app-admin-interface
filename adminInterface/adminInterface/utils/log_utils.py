from os import environ
from sentry_sdk import capture_message


def log_message(message):
    """
    Logs the provided message to sentry if the environment is
    production. Otherwise the message is printed to the console

    Parameters:

    message (string): The message that should be logged
    """
    environment = environ.get('DJANGO_SETTINGS_MODULE')
    if environment == 'adminInterface.settings.production':
        capture_message(message)
    else:
        print(message)
