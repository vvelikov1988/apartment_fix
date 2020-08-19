from django.db import models
from datetime import date, datetime
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register_validator(self, formData):
        errors = {}
        check = User.objects.filter(email=formData['email'])
        if len(formData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters long."
        if len(formData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters long."
        if len(formData['password']) < 8:
            errors['password'] = "Password cannot be less than 8 characters."
        elif formData['password'] != formData['confirm_password']:
            errors['password'] = "Passwords do not match."
        if len(formData['email']) < 1:
            errors['reg_email'] = "Email address cannot be blank."
        elif not EMAIL_REGEX.match(formData['email']):
            errors['reg_email'] = "Please enter a valid email address."
        elif check:
            errors['reg_email'] = "Email address is already registered."
        return errors
    
    def login_validator(self, loginData):
        errors = {}
        check = User.objects.filter(email=loginData['login_email'])
        if not check:
            errors['login_email'] = "Email has not been registered."
        else:
            if not bcrypt.checkpw(loginData['login_password'].encode(), check[0].password.encode()):
                errors['login_email'] = "Email and password do not match."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

# class TripManager(models.Manager):
#     def trip_validation(self, tripData):
#         today = datetime.now()
#         errors = {}
#         if len(tripData['dest']) < 3:
#             errors['dest'] = "Destination must be at least 3 characters"
#         if len(tripData['plan']) < 10:
#             errors['plan'] = "You need a better plan :)"
#         if len(tripData['tripstartdate']) < 1:
#             errors['tripstartdate'] = "Please select valid start date"
#         elif datetime.strptime(tripData['tripstartdate'], "%Y-%m-%d") < today:
#             errors['tripstartdate'] = "Your trip can not start in the past"
#         if len(tripData['tripenddate']) < 1:
#             errors['tripenddate'] = "Please select valid end date"        
#         elif tripData['tripstartdate'] > tripData['tripenddate']:
#             errors['tripenddate'] = "No Time Travel allowed :)"
#         return errors
class IssueManager(models.Manager):
    def issue_validation(self, issueData):
        today = datetime.now()
        errors = {}
        if len(issueData['title']) < 3:
            errors['title'] = "Title must be at least 3 characters."
        elif len(issueData['title']) > 255:
            errors['title'] = "Title must be shorter than 255 characters."
        if len(issueData['description']) < 10:
            errors['description'] = "Please provide a more detailed description."
        if len(issueData['target']) < 1:
            errors['target'] = "Please select valid target date"
        elif datetime.strptime(issueData['target'], "%Y-%m-%d") < today:
            errors['target'] = "Your target date can not be in the past"
        return errors

# class Trip(models.Model):
#     destination = models.CharField(max_length=255)
#     start_dt = models.DateField()
#     end_dt = models.DateField()
#     plan = models.TextField()
#     created_by = models.ForeignKey(User, related_name="user_trips", on_delete=models.CASCADE)
#     joined_by = models.ManyToManyField(User, related_name="joined_trips")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     objects = TripManager()


class Issue(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    completed_at = models.DateField(auto_now=True)
    target_dt = models.DateField()
    created_by = models.ForeignKey(User, related_name="user_issues", on_delete = models.CASCADE)
    volunteers = models.ManyToManyField(User, related_name="user_volunteers")
    objects = IssueManager()

