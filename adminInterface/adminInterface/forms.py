from django.forms import ModelForm
from adminInterface.models import Event
from django import forms
from adminInterface.utils import Firestore


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
