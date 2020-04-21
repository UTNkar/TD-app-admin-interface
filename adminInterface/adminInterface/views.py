import os
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import firebase_admin
from firebase_admin import firestore

firebase_admin.initialize_app()
db = firestore.client()

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

def login_user(request):
    uname = request.POST.get('username')
    passw = request.POST.get("pass")
    user = authenticate(request, username=uname, password=passw)
    if user is not None:
        login(request, user)
        return redirect('/start')
    else:
        message = "invalid cerediantials"
        return redirect('/')
        
    
    
        

