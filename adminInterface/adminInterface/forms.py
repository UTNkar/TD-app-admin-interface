from django.forms import ModelForm
from adminInterface.models import Event, Notification, Section
from django import forms
from adminInterface.utils.firebase_utils import Firestore, CloudMessaging
import datetime
from adminInterface.fields import DataListWidget
import numpy as np
from math import ceil
from sentry_sdk import capture_exception


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
    class Meta:
        model = Notification
        fields = ['title',
                  'body',
                  'sender',
                  'who'
                  ]
    SENDER_CHOICES = [
        'Rekå',
        'Fadderkå',
        'Mediakå',
        'UTN',
    ]

    sender = forms.CharField(
        max_length=50,
        widget=DataListWidget(
            data_list=SENDER_CHOICES,
            name="sender"
        )
    )

    def save(self):
        data = self.cleaned_data
        messaging = CloudMessaging.get_instance()

        who = data.get('who')
        db = Firestore.get_instance()
        section_ref = db.collection('users').where('userClass', 'in', who)
        docs = section_ref.stream()

        registration_tokens = []
        for doc in docs:
            doc = doc.to_dict()
            registration_token = doc.get("userToken")

            if registration_token:
                registration_tokens.append(registration_token)

        new_docs = np.array(registration_tokens)

        # A multicast message can only be sent to up to 100 registration
        # tokens at a time. We therefor split the user's registration tokens
        # into arrays with a maximum length of 99 just to have a safe margin
        number_of_slices = ceil(new_docs.size / 99)
        users_chunks = np.array_split(new_docs, number_of_slices)

        # date without 0 / month without 0
        time_now = datetime.datetime.now()
        senderDate = time_now.strftime("%-d/%-m")

        for users_chunk in users_chunks:
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=data.get('title'),
                    body=data.get('body'),
                ),
                data={
                    'title': data.get('title'),
                    'body': data.get('body'),
                    'sender': data.get('sender'),
                    'senderDate': senderDate
                },
                tokens=users_chunk.tolist(),
            )
            try:
                response = messaging.send_multicast(message)
                print(
                    '{0} messages were sent successfully'.format(
                        response.success_count
                    )
                )
                print('{0} messages failed'.format(response.failure_count))
                if response.failure_count > 0:
                    for sendResponse in response.responses:
                        if not sendResponse.success:
                            print(sendResponse.exception)
            except Exception as error:
                capture_exception(error)
