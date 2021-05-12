from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
from datetime import datetime
import bcrypt

# Create your views here.
def index(request):
    return render(request, "index.html")

def success(request):
    if 'userid' in request.session.keys():
        return render(request, "success.html")
    else:
        return HttpResponse("<h1>Access Denied</h1>")

def register_user(request):
    all_users_emails = []
    for user in User.objects.all():
        all_users_emails.append(user.email)
    if request.method == "POST":
        errors = User.objects.register_validator(request.session, request.POST, all_users_emails)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='register')
            return redirect('/')
        else:
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            birth_date = request.POST["birth_date"]
            email = request.POST["email"]
            password = request.POST["password"]
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            new_user = User.objects.create(first_name = first_name, last_name = last_name, birth_date = birth_date, email = email, password = pw_hash)
            request.session['userid'] = new_user.id
            request.session['username'] = new_user.first_name
            request.session['in'] = 'registered'
            return redirect("/success/")

def login_user(request):
    all_users_emails = []
    for user in User.objects.all():
        all_users_emails.append(user.email)
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email_login'])
        errors = User.objects.login_validator(request.session, request.POST, all_users_emails)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags='login')
            return redirect('/')
        if user: 
            logged_user = user[0] 
            if bcrypt.checkpw(request.POST['password_login'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                request.session['username'] = logged_user.first_name
                request.session['in'] = 'logged in'
                return redirect('/success')
            else:
                messages.error(request, 'Wrong password', extra_tags='login')
                return redirect("/")

def logout_user(request):
    request.session.flush()
    return redirect("/")