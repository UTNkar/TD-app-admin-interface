import pyrebase
import os
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
#from django.contrib.sessions.backends.db import SessionStore


config = {
'apiKey': os.environ.get("FIREBASE_APIKEY"),
'authDomain': os.environ.get("FIREBASE_AUTHDOMAIN"),
'databaseURL': os.environ.get("FIREBASE_DATABASEURL"),
'projectId': os.environ.get("FIREBASE_PROJECTID"),
'storageBucket': os.environ.get("FIREBASE_STORGAEBUCKET")
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def singIn(request):
    request.session['signed_in'] = False
    return render(request, "signIn.html")

@login_required
def events(request):
    db.child("users").child("Joe")
    return render(request, "events.html")

@login_required
def start(request):
    return render(request, "welcome.html")

def postsign(request):
    uname = request.POST.get('username')
    passw = request.POST.get("pass")
    user = authenticate(request, username=uname, password=passw)
    if user is not None:
        login(request, user)

        return redirect('/postsign/start')
    else:
        message = "invalid cerediantials"
        return redirect('/')
        
    
    
        

