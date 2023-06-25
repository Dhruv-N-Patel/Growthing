from .models import Project, Roadmap
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import os
import openai
from dotenv import load_dotenv, find_dotenv
from django.contrib import messages

# Create your views here.
def project_list(request):
    projects = Project.objects.all()
    # project_data = [{'title': project.title, 'description': project.description, 'skills': project.skills} for project in projects]
    programming = Project.objects.filter(genre='programming')
    design = Project.objects.filter(genre='design')
    marketing = Project.objects.filter(genre='marketing')
    video_editing = Project.objects.filter(genre='video editing')
    misc = Project.objects.filter(genre='misc')
    return render(request, "explore.html", context={'projects':projects, 'programming':programming, 'design':design,'marketing':marketing,'video_editing':video_editing, 'misc':misc})

def explore(request):
    context={
        
    }
    return render(request, "explore.html", context)

def assistant(request):
    context={
    "previos_chatings1":"this is your previous chattings"
    }
    return render(request,'assistant.html', context)
    # return HttpResponse("hey I am assistant")

def ongoing(request): 
    context={
        "My_projects":"all my projects will be shown here"
    }
    return render(request,'ongoing.html', context)

def index(request):
    context={
        "index_content":'index ka content'
    }
    messages.success(request, 'this is test message')
    return render(request, 'index.html', context)

def project_content(request):
    projects = Project.objects.all()
    # programming = Project.objects.filter(tag='programming') 
    # design = Project.objects.filter(tag='design')
    # marketing = Project.objects.filter(tag='marketing')
    # video_editing = Project.objects.filter(tag='video editing')
    # misc = Project.objects.filter(tag='misc')
    project_data = [{'title': project.title, 'description': project.description, 'skills': project.skills, 'id':project.project_id} for project in projects]
    project_pro001 = Project.objects.filter(project_id='pro001')

    # return render(request, "explore.html", context={'projects':projects, 'programming':programming, 'design':design,'marketing':marketing,'video_editing':video_editing, 'misc':misc})

    return render(request,'project.html', context={'project_pro001':project_pro001,'content':project_data })

def generate_roadmap(request):
    # Retrieve projects from the database
    projects = Project.objects.all()

    # Prepare input data for OpenAI API
    input_data = ""
    for project in projects:
        input_data += f"Project Title: {project.title}\n"
        input_data += f"Project Description: {project.description}\n"
        input_data += f"Skills: {project.skills}\n\n"

    # Make request to OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"make roadmap of the project title whose discription is Project Description and which involve Skills",
        max_tokens=500,  # Adjust the token count as per your needs
        temperature=0.1,  # Adjust the temperature value for desired creativity
        n=1,  # Adjust the 'n' value to control the number of responses generated
        stop=None,
    )

    # Process the API response
    generated_roadmap = response.choices[0].text.strip()

    # Save the roadmap in the 'roadmap' database
    roadmap = Roadmap(
        project_name=projects[0].title,  # g there's only one project for simplicity
        roadmap=generated_roadmap,
    )
    roadmap.save()

    return render(request, 'generate_roadmap.html', {'roadmap': roadmap})