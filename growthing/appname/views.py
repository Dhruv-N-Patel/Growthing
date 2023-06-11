from .models import Project
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def project_list(request):
    projects = Project.objects.all()
    project_data = [{'title': project.title, 'description': project.description, 'skills': project.skills} for project in projects]
    return JsonResponse(project_data, safe=False)