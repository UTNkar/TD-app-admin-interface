from django.db import models
from multiselectfield import MultiSelectField


# class Section(models.Model):
#     classes = models.ArrayField(ArrayField(CharField(max_length=30)))


# lägg till alla klasser
CLASS_CHOICES = [
    ('IT1a', 'IT1a'),
    ('IT1b', 'IT1b'),
    ('IT1c', 'IT1c'),
]


class Event(models.Model):
    name = models.CharField(max_length=30)
    disappear = models.DateTimeField(editable=True)
    form = models.CharField(max_length=30)
    release = models.DateTimeField(editable=True)
    who = MultiSelectField(choices=CLASS_CHOICES)

