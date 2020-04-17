import pyrebase
import os
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


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
    return render(request, "signIn.html")

@login_required
def ticket_system(request):
    users = db.child("event/klassfesttest").get()
    print(users.val()) # {"Morty": {"name": "Mortimer 'Morty' Smith"}, "Rick": {"name": "Rick Sanchez"}}
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
        
    
    
        

