from django.forms import ModelForm
from adminInterface.models import Event, Notification, Section
from django import forms
from adminInterface.firebase_utils import Firestore, CloudMessaging
import datetime


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
                  'senderDate',
                  'who'
                  ]

    def save(self):
        data = self.cleaned_data
        messaging = CloudMessaging.get_instance()

        db = Firestore.get_instance()
        section_ref = db.collection('users')
        docs = section_ref.stream()

        who = data.get('who')
        registration_tokens = []

        for user in docs:
            user_fields = user.to_dict()
            user_class_name = user_fields.get('userClass')
            for who_class_name in who:
                if who_class_name == user_class_name:
                    token = user_fields.get('userToken')
                    if len(token) > 0:
                        registration_tokens.append(token)

        time_now = datetime.datetime.now()
        senderDate = time_now.date() + "/" + time_now.month()

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
            tokens=registration_tokens,
        )
        response = messaging.send_multicast(message)
        # See the BatchResponse reference documentation
        # for the contents of response.
        print('{0} messages were sent successfully'.format(response.
                                                           success_count))
