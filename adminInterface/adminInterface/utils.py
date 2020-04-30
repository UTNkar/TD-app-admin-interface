import firebase_admin
from firebase_admin import firestore


class Firestore:
    dataBase = None
    @staticmethod
    def get_instance():
        if Firestore.dataBase is None:
            firebase_admin.initialize_app()
            Firestore.dataBase = firestore.client()
        return Firestore.dataBase
