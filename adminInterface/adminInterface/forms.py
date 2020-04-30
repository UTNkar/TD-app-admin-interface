from django.forms import ModelForm
from adminInterface.models import Section
from adminInterface.utils import Firestore
from django import forms


class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ['firebase_id', 'sectionName', 'sectionFullName']
        widgets = {'firebase_id': forms.HiddenInput()}

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
