from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),  #register and login screen
    path('welcome', views.welcome),  #welcome screen - user dashboard template
    path('login', views.login), #login function
    path('logout', views.logout), #logout function
    path('register', views.register), #register function
    path('dashboard', views.dashboard), #open issues template
    path('details/<int:issue_id>', views.details), #issue details template
    path('signup/<int:issue_id>', views.assign_volunteer), #function for user volunteering for an issue
    # path('completed', views.completed), #completed issues
    path('open', views.open), #open new issue template
    path('create', views.create), #create an issue function		   
]