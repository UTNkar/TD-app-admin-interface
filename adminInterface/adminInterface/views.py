from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
import firebase_admin
from firebase_admin import firestore
from adminInterface.utils import Firestore



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
        sections.append(doc_fields)
       
    print(sections)
    return render(request, "sections.html", {"sections": sections})


def login_user(request):
    uname = request.POST.get('username')
    passw = request.POST.get("pass")
    user = authenticate(request, username=uname, password=passw)
    if user is not None:
        login(request, user)
        return redirect('/start')
    else:
        return redirect('/')
