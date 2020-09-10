from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from adminInterface.models import Event, Section
from adminInterface.forms import EventForm, NotificationForm, SectionForm
from adminInterface.utils.firebase_utils import Firestore
from django.contrib import messages


def singIn(request):
    """
    Redirects to the first page when signed in
    """
    current_user = request.user
    if current_user.is_authenticated:
        return redirect('/start')
    else:
        return render(request, "signIn.html")


@login_required
def create_notification(request):
    """
    Redirects to a page where it is possible to create a notification
    """
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            statistics = form.save()

            messages.info(
                request,
                'Notisen skickades till {0} användare'.format(
                    statistics.get("success_count")
                )
            )

            messages.info(
                request,
                'Notisen misslyckades att skickas till {0} användare'.format(
                    statistics.get("failure_count")
                )
            )

            if statistics.get("batches_failed") > 0:
                messages.info(
                    request,
                    '{0} batches failed'.format(
                        statistics.get("batches_failed")
                    )
                )

            if len(statistics.get("error_reasons_counted")) > 0:
                messages.info(
                    request,
                    'Orsaker till utskicket misslyckades:'
                )

            for exception, amount in statistics.get("error_reasons_counted"):
                messages.info(
                    request,
                    '{0}: {1}'.format(exception, amount)
                )

            return redirect('/notifications/')
    else:
        form = NotificationForm()
    return render(request, "create_notification.html", {'form': form})


@login_required
def delete_event(request, id):
    """
    Redirects back to the event page when an event has been deleted

    Parameters:

    id (int): ID of the event that has been deleted
    """
    db = Firestore.get_instance()
    event_ref = db.collection(u'event').document(id)
    event_ref.delete()
    return redirect('/ticket-system/')


@login_required
def create_event(request):
    """
    Redirects to a page where it is possible to create an event
    """
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
    """
    Redirects to a page where it is possible to edit an event

    Parameters:

    id (int): ID of the event to be edited
    """
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
    """
    Redirects to a page that shows all events
    """
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

    events.sort(key=lambda item: item.name)

    return render(request,
                  "ticket-system.html",
                  {"events": events})


@login_required
def start(request):
    """
    Shows the start page where it is possible to sign in
    """
    return render(request, "welcome.html")


@login_required
def sections(request):
    """
    Redirects to a page that shows all sections
    """
    db = Firestore.get_instance()
    section_ref = db.collection('sections')
    section_docs = section_ref.stream()
    sections = []

    for doc in section_docs:
        doc_fields = doc.to_dict()
        classNames = []

        classes = doc_fields.get('classes', [])
        for this_class in classes:
            classNames.append(this_class.get("className"))

        classes_string = ",".join(classNames)

        section = Section(
            firebase_id=doc.id,
            sectionName=doc_fields.get('sectionName'),
            sectionFullName=doc_fields.get('sectionFullName'),
            classes=classes_string
        )
        sections.append(section)

    sections.sort(key=lambda item: item.sectionName)

    return render(request, "sections.html", {"sections": sections})


@login_required
def create_section(request):
    """
    Redirects to a page where it is possible to create a section
    """
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
    """
    Redirects to a page where it is possible to edit a section

    Parameters:

    id (int): ID of the section to be edited
    """
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
    """
    Redirects back to the section page when a section has been deleted

    Parameters:

    id (int): ID of the section that has been deleted
    """
    db = Firestore.get_instance()
    section_ref = db.collection('sections').document(id)
    section_ref.delete()
    return redirect('/sections')


def login_user(request):
    """
    Authenticates the user. A successful login redirects to the first page when signed in. An unsuccessful login redirects back to the start page where it is possible to sign in.
    """
    uname = request.POST.get('username')
    passw = request.POST.get("pass")
    user = authenticate(request, username=uname, password=passw)
    if user is not None:
        login(request, user)
        return redirect('/start')
    else:
        return redirect('/')
