from django.forms import ModelForm
from adminInterface.models import Event, Notification, Section
from django import forms
from adminInterface.firebase_utils import Firestore, CloudMessaging


class SectionForm(ModelForm):

    firebase_id = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Section
        fields = ['firebase_id', 'sectionName', 'sectionFullName']

    def save(self):
        data = self.cleaned_data
        db = Firestore.get_instance()
        id = data.get('firebase_id')
        if id:
            doc_ref = db.collection(u'sections').document(id)
        else:
            doc_ref = db.collection(u'sections').document()
        doc_ref.set({
            u'sectionName': data.get('sectionName'),
            u'sectionFullName': data.get('sectionFullName')
        })
        return data


class EventForm(ModelForm):

    disappear = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        )
    )
    release = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        )
    )

    firebase_id = forms.CharField(
        widget=forms.HiddenInput(),
        required=False
    )

    class Meta:
        model = Event
        fields = ['firebase_id',
                  'name',
                  'disappear',
                  'form',
                  'release',
                  'who']

    def save(self):
        data = self.cleaned_data
        db = Firestore.get_instance()
        id = data.get('firebase_id')
        if id:
            doc_ref = db.collection(u'event').document(id)
        else:
            doc_ref = db.collection(u'event').document()
        doc_ref.set({
            u'name': data.get('name'),
            u'disappear': data.get('disappear'),
            u'form': data.get('form'),
            u'release': data.get('release'),
            u'who': data.get('who')
        })
        return data


class NotificationForm(ModelForm):
    senderDate = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        )
    )

    class Meta:
        model = Notification
        fields = ['title',
                  'body',
                  'sender',
                  'senderDate',
                  'notification',
                  'who'
                  ]

    def save(self):
        data = self.cleaned_data
        messaging = CloudMessaging.get_instance()
        topic = 'highScores'
        # condition = "'stock-GOOG' in topics || 'industry-tech' in topics"

        # See documentation on defining a message payload.
        message = messaging.Message(
            notification=messaging.Notification(
                title=data.get('title'),
                body=data.get('body'),
            ),
            # condition=condition,
            topic=topic
        )

        # Send a message to devices subscribed to the combination of topics
        # specified by the provided condition.
        response = messaging.send(message)
        # Response is a message ID string.
        print('Successfully sent message:', response)
