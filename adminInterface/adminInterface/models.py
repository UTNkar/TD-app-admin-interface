from django.db import models
from adminInterface.utils.firebase_utils import Firestore


class Section(models.Model):
    class Meta:
        managed = False

    firebase_id = models.CharField(max_length=60)
    sectionName = models.CharField(max_length=5)
    sectionFullName = models.CharField(max_length=60)
    classes = models.CharField(max_length=60)

    @staticmethod
    def get_all_classes():
        db = Firestore.get_instance()
        section_ref = db.collection('sections')
        docs = section_ref.get()
        classes = []

        for section in docs:
            section_fields = section.to_dict()
            section_classes = section_fields.get('classes')
            if section_classes is not None:
                for section_class in section_classes:
                    class_name = section_class.get('className')
                    classes.append(class_name)

        classes.sort(key=str.casefold)

        return classes

    @staticmethod
    def get_all_classes_tuple():
        classes = Section.get_all_classes()
        classes_tuple = []

        for class_name in classes:
            class_name_tuple = (str(class_name), str(class_name))
            classes_tuple.append(class_name_tuple)

        return classes_tuple


class Event(models.Model):
    class Meta:
        managed = False

    firebase_id = models.CharField(max_length=100)
    name = models.CharField(max_length=30)
    disappear = models.DateTimeField(editable=True)
    form = models.URLField()
    release = models.DateTimeField(editable=True)
    who = models.CharField(max_length=100)


class Notification(models.Model):
    class Meta:
        managed = False

    title = models.CharField(max_length=65, help_text='Max 65 tecken')
    body = models.CharField(max_length=240, help_text='Max 240 tecken')
    sender = models.CharField(max_length=50)
    senderDate = models.CharField(max_length=8)
    who = models.CharField(max_length=500)
