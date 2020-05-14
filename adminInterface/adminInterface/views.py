from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from adminInterface.utils import Firestore
from adminInterface.models import Section
from adminInterface.forms import SectionForm



def singIn(request):
    return render(request, "signIn.html")


@login_required
def ticket_system(request):
    users_ref = db.collection(u'event')
    docs = users_ref.stream()

    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
    return render(request, "ticket-system.html")


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
        section = Section(
            firebase_id=doc.id,
            sectionName=doc_fields.get('sectionName'),
            sectionFullName=doc_fields.get('sectionFullName')
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
    return render(request, 'create_section.html', {"form": sec_form})


@login_required
def edit_section(request, id):
    db = Firestore.get_instance()
    section_ref = db.collection('sections').document(id)
    section = section_ref.get()
    sec = section.to_dict()

    s = Section(
        firebase_id=id,
        sectionName=sec.get('sectionName'),
        sectionFullName=sec.get('sectionFullName')
    )
    sec_form = SectionForm(request.POST, instance=s)
    if request.method == 'POST':
        if sec_form.is_valid():
            sec_form.save()
            return redirect('/sections')

    else:
        sec_form = SectionForm(instance=s)
    return render(request, 'edit_section.html', {"form": sec_form})

@login_required
def delete_section(request, id):
    db = Firestore.get_instance()
    section_ref = db.collection('sections').document(id)
    section_ref.delete()
    return redirect ('/sections')

def login_user(request):
    uname = request.POST.get('username')
    passw = request.POST.get("pass")
    user = authenticate(request, username=uname, password=passw)
    if user is not None:
        login(request, user)
        return redirect('/start')
    else:
        return redirect('/')
