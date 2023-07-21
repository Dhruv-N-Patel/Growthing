from django.urls import path
from . import views
from django.urls import path
from django.urls import path
# from .views import ClearChatView
from appname.views import project_list
from appname.views import generate_roadmap
from django.contrib import admin
from django.urls import path, include
from appname import views
# from .views import ResumeAssistantView, 
urlpatterns = [
    # path('resume-assistant/', ResumeAssistantView.as_view(), name='resume_assistant'),
    # path('clear-chat/', ClearChatView.as_view(), name='clear_chat'),
    path('', views.index, name='index' ),
    path('home/', views.ongoing, name='ongoing_project_list'),
    path('home/', views.home, name='home'),
    path('explore/', project_list, name='project_list'),
    path("assistant/",views.assistant,name='assistant'),
    path("project/<str:pk>/", views.project_content, name="project"),
    path("<str:username>/generate_roadmap/<str:pk>/", views.generate_roadmap, name="generate_roadmap"),
    path("<str:username>/roadmap/<str:pk>/", views.show_roadmap, name="roadmap"),
    path("project/<str:pk>/", views.show_roadmap, name="project"),
    path("signup/", views.signup, name="signup"),
    # path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
]