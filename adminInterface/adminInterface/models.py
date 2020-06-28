from django.db import models
from multiselectfield import MultiSelectField
from adminInterface.utils import Firestore


class Section(models.Model):
    firebase_id = models.CharField(max_length=60)
    sectionName = models.CharField(max_length=5)
    sectionFullName = models.CharField(max_length=60)
    classes = models.CharField(max_length=60)

    @staticmethod
    def get_all_classes():
        db = Firestore.get_instance()
        section_ref = db.collection('sections')
        docs = section_ref.stream()
        classes = []

        for section in docs:
            section_fields = section.to_dict()
            section_classes = section_fields.get('classes')
            if section_classes is not None:
                for section_class in section_classes:
                    class_name = section_class.get('className')
                    classes.append(class_name)

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
    firebase_id = models.CharField(max_length=100)
    name = models.CharField(max_length=30)
    disappear = models.DateTimeField(editable=True)
    form = models.CharField(max_length=30)
    release = models.DateTimeField(editable=True)
    who = MultiSelectField(choices=Section.get_all_classes_tuple())
