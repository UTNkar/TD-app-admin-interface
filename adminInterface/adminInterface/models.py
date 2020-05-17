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
    firebase_id = models.CharField(max_length=100)
    name = models.CharField(max_length=30)
    disappear = models.DateTimeField(editable=True)
    form = models.CharField(max_length=30)
    release = models.DateTimeField(editable=True)
    who = MultiSelectField(choices=CLASS_CHOICES)


class Notification(models.Model):
    SENDER_CHOICES = [
        ('Rekå', 'Rekå'),
        ('Fadderkå', 'Fadderkå'),
        ('Mediakå', 'Mediakå'),
        ('UTN', 'UTN'),
    ]
    title = models.CharField(max_length=30)
    body = models.CharField(max_length=300)
    sender = models.CharField(max_length=8, choices=SENDER_CHOICES)
    senderDate = models.DateTimeField(editable=True)
    notification = models.CharField(max_length=30)
    who = MultiSelectField(choices=CLASS_CHOICES)
