from .models import Project
from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def project_list(request):
    projects = Project.objects.all()
    project_data = [{'title': project.title, 'description': project.description, 'skills': project.skills} for project in projects]
    programming = Project.objects.filter(tag='programming')
    design = Project.objects.filter(tag='design')
    marketing = Project.objects.filter(tag='marketing')
    video_editing = Project.objects.filter(tag='video editing')
    misc = Project.objects.filter(tag='misc')
    # return JsonResponse(project_data, safe=False)
    return render(request, "explore.html", context={'projects':projects, 'programming':programming, 'design':design,'marketing':marketing,'video_editing':video_editing, 'misc':misc})