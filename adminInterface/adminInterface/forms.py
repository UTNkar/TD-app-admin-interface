from django.forms import ModelForm
from adminInterface.models import Event, Notification, Section
from django import forms
from adminInterface.utils.firebase_utils import Firestore, CloudMessaging
from adminInterface.fields import DataListWidget


class SectionForm(ModelForm):

    firebase_id = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Section
        fields = ['firebase_id', 'sectionName', 'sectionFullName', 'classes']

    def save(self):
        data = self.cleaned_data
        db = Firestore.get_instance()
        id = data.get('firebase_id')
        class_list = []
        classes_split = data.get('classes').split(',')
        for class_name in classes_split:
            class_list.append({'className': class_name})

        if id:
            doc_ref = db.collection(u'sections').document(id)
        else:
            doc_ref = db.collection(u'sections').document()

        doc_ref.set({
            u'sectionName': data.get('sectionName'),
            u'sectionFullName': data.get('sectionFullName'),
            u'classes': class_list
        })
        return data


class EventForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields["who"] = forms.MultipleChoiceField(
            choices=Section.get_all_classes_tuple(),
            widget=forms.CheckboxSelectMultiple
        )

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

    # The number of classes can change during runtime and therefor we must
    # add it dynamically
    def __init__(self, *args, **kwargs):
        super(NotificationForm, self).__init__(*args, **kwargs)
        self.fields["who"] = forms.MultipleChoiceField(
            choices=Section.get_all_classes_tuple(),
            widget=forms.CheckboxSelectMultiple
        )

    def save(self):
        data = self.cleaned_data

        classes = data.get('who')

        registration_tokens = Firestore\
            .get_user_registration_tokens_by_classes(classes)

        response = CloudMessaging.send_notification(
            registration_tokens,
            data.get("title"),
            data.get("body"),
            data.get("sender")
        )

        return response
