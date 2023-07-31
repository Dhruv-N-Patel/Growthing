from appname.views import project_list
from appname.views import generate_roadmap
from django.contrib import admin
from django.urls import path, include
from appname import views
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Default authentication views for normal users
    path('', include('appname.urls')), 
]