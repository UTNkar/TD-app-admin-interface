from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from adminInterface.utils import Firestore
from adminInterface.models import Section
from adminInterface.forms import SectionForm
from adminInterface.models import Event
from adminInterface.forms import EventForm


def singIn(request):
    current_user = request.user
    if current_user.is_authenticated:
        return redirect('/start')
    else:
        return render(request, "signIn.html")


@login_required
def delete_event(request, id):
    db = Firestore.get_instance()
    event_ref = db.collection(u'event').document(id)
    event_ref.delete()
    return redirect('/ticket-system/')


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/ticket-system/')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})


@login_required
def edit_event(request, id):
    db = Firestore.get_instance()
    event_ref = db.collection(u'event').document(id)
    event = event_ref.get()
    doc_fields = event.to_dict()
    event_object = Event(
            firebase_id=id,
            name=doc_fields.get('name'),
            disappear=doc_fields.get('disappear'),
            form=doc_fields.get('form'),
            release=doc_fields.get('release'),
            who=doc_fields.get('who')
        )
    form = EventForm(request.POST, instance=event_object)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('ticket-system/')
    else:
        form = EventForm(instance=event_object)
    return render(request, 'create_event.html', {'form': form,
                                                 'edit_event': True})


@login_required
def ticket_system(request):
    db = Firestore.get_instance()
    events_ref = db.collection(u'event')
    docs = events_ref.stream()
    events = []

    for doc in docs:
        doc_fields = doc.to_dict()
        event = Event(
            firebase_id=doc.id,
            name=doc_fields.get('name'),
            disappear=doc_fields.get('disappear'),
            form=doc_fields.get('form'),
            release=doc_fields.get('release'),
            who=doc_fields.get('who')
        )
        events.append(event)
    return render(request,
                  "ticket-system.html",
                  {"events": events})


@login_required
def start(request):
    return render(request, "welcome.html")


@login_required
def sections(request):
    db = Firestore.get_instance()
    section_ref = db.collection('sections')
    classes_docs = section_ref.stream()
    sections = []

    for doc in classes_docs:
        doc_fields = doc.to_dict()
        classNames = []

        if doc_fields.get('classes') is not None:
            for i in doc_fields.get('classes'):
                classNames.append(i.get("className"))

        classes_string = ",".join(classNames)

        section = Section(
            firebase_id=doc.id,
            sectionName=doc_fields.get('sectionName'),
            sectionFullName=doc_fields.get('sectionFullName'),
            classes=classes_string
        )
        sections.append(section)

    return render(request, "sections.html", {"sections": sections})


@login_required
def create_section(request):
    if request.method == 'POST':
        sec_form = SectionForm(request.POST)
        if sec_form.is_valid():
            sec_form.save()
            return redirect('/sections')

    else:
        sec_form = SectionForm()
    return render(request, 'create_section.html', {'form': sec_form})


@login_required
def edit_section(request, id):
    db = Firestore.get_instance()
    section_ref = db.collection('sections').document(id)
    section = section_ref.get()
    sec = section.to_dict()

    classNames = []
    for i in sec.get("classes"):
        classNames.append(i.get("className"))

    classes_string = ",".join(classNames)

    s = Section(
        firebase_id=id,
        sectionName=sec.get('sectionName'),
        sectionFullName=sec.get('sectionFullName'),
        classes=classes_string
    )

    sec_form = SectionForm(request.POST, instance=s)
    if request.method == 'POST':
        if sec_form.is_valid():
            sec_form.save()
            return redirect('/sections')

    else:
        sec_form = SectionForm(instance=s)
    return render(request, 'create_section.html', {'form': sec_form,
                                                   'edit_section': True})


@login_required
def delete_section(request, id):
    db = Firestore.get_instance()
    section_ref = db.collection('sections').document(id)
    section_ref.delete()
    return redirect('/sections')


def login_user(request):
    uname = request.POST.get('username')
    passw = request.POST.get("pass")
    user = authenticate(request, username=uname, password=passw)
    if user is not None:
        login(request, user)
        return redirect('/start')
    else:
        return redirect('/')
