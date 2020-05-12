from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from adminInterface.models import Event
from adminInterface.forms import EventForm
from adminInterface.utils import Firestore


def singIn(request):
    return render(request, "signIn.html")


@login_required
def notifications(request):
    return render(request, "create_notification.html")


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


def login_user(request):
    uname = request.POST.get('username')
    passw = request.POST.get("pass")
    user = authenticate(request, username=uname, password=passw)
    if user is not None:
        login(request, user)
        return redirect('/start')
    else:
        return redirect('/')
