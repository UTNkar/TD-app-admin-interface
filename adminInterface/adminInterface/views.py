import pyrebase
import os
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


config = {
'apiKey': os.environ.get("FIREBASE_APIKEY"),
'authDomain': os.environ.get("FIREBASE_AUTHDOMAIN"),
'databaseURL': os.environ.get("FIREBASE_DATABASEURL"),
'projectId': os.environ.get("FIREBASE_PROJECTID"),
'storageBucket': os.environ.get("FIREBASE_STORGAEBUCKET")
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
def singIn(request):
    request.session['signed_in'] = False
    return render(request, "signIn.html")


def page2(request):
    return render(request, "page2.html")


def start(request):
    return render(request, "welcome.html")

def postsign(request):
    email=request.POST.get('email')
    passw = request.POST.get("pass")
    signed_in = request.session.get('signed_in', False)
    if signed_in == False:
        try:
            user = auth.sign_in_with_email_and_password(email,passw)
            request.session['signed_in'] = True
        except:
            message = "invalid cerediantials"
            return redirect('/')
    
    return redirect('/postsign/start')
        

