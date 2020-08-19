from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Issue
import bcrypt

def index(request):
    return render(request, "index.html")

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/welcome')

def logout(request):
    request.session.clear()
    return redirect ('/')

def welcome(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        user_issues = Issue.objects.filter(created_by=request.session["user_id"])
        volunteered_issues = Issue.objects.filter(volunteers=request.session["user_id"])
        context = {
            "user_issues": user_issues,
            "volunteered_issues" : volunteered_issues
            }
    return render(request, "welcome.html", context)

def dashboard(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        context = {
            "all_issues": Issue.objects.all
            }
    return render(request, "dashboard.html", context)


def open(request):
    return render(request, "openissue.html")

def create(request):
    errors = Issue.objects.issue_validation(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/open')
    else:
        user = User.objects.get(id=request.session["user_id"])
        issue = Issue.objects.create(
            title = request.POST['title'],
            description = request.POST['description'],
            target_dt = request.POST['target'],
            created_by = user
        )
        return redirect('/welcome')

def details(request, issue_id):
    issue = Issue.objects.get(id=issue_id)
    context = {
        "issue" : issue
    }
    return render(request, "details.html", context)

def assign_volunteer(request, issue_id):
    issue = Issue.objects.get(id=issue_id)
    volunteer = User.objects.get(id=request.session["user_id"])
    issue.volunteers.add(volunteer)
    return redirect('/welcome')