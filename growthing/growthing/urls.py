"""
URL configuration for growthing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from appname.views import project_list
from appname.views import generate_roadmap
from django.contrib import admin
from django.urls import path
from appname import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('explore/', project_list, name='project_list'),
    path("assistant/",views.assistant,name='assistant'),
    path('ongoing/', views.ongoing, name='ongoing'),
    path('', views.index, name='index' ),
    path("project/<str:pk>/", views.project_content, name="project"),
    path("roadmap/<str:pk>/", views.generate_roadmap, name="roadmap"),
    path("project/<str:pk>/", views.show_roadmap, name="project"),
    # path("roadmap/<str:pk>/", views.show_roadmap, name="roadmap"),
    # path('roadmap/', views.roadmap,name='roadmap')
]