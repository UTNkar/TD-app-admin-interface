import pyrebase
import os
from django.shortcuts import render 

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
    return render(request, "signIn.html")

def postsign(request):
    email=request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = auth.sign_in_with_email_and_password(email,passw)
    except:
        message = "invalid cerediantials"
        return render(request,"signIn.html",{"msg":message})
    print(user)
    return render(request, "welcome.html",{"e":email})