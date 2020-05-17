import firebase_admin
from firebase_admin import firestore
from firebase_admin import messaging


class Firebase:
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
