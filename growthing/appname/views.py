from .models import Project, Roadmap
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import os
import openai
from dotenv import load_dotenv, find_dotenv
from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect

# Create your views here.
def project_list(request):
    projects = Project.objects.all()
    programming = Project.objects.filter(genre='programming')
    design = Project.objects.filter(genre='design')
    marketing = Project.objects.filter(genre='marketing')
    video_editing = Project.objects.filter(genre='video editing')
    misc = Project.objects.filter(genre='misc')
    return render(request, "explore.html", context={'projects':projects, 'programming':programming, 'design':design,'marketing':marketing,'video_editing':video_editing, 'misc':misc})

def ongoing_project_list(request):
    projects = Roadmap.objects.all()
    programming = Roadmap.objects.filter(genre='programming')
    design = Roadmap.objects.filter(genre='design')
    marketing = Roadmap.objects.filter(genre='marketing')
    video_editing = Roadmap.objects.filter(genre='video editing')
    misc = Roadmap.objects.filter(genre='misc')
    return render(request, "myhome.html", context={'projects':projects, 'programming':programming, 'design':design,'marketing':marketing,'video_editing':video_editing, 'misc':misc})

def explore(request):
    context={
        
    }
    return render(request, "explore.html", context)

def assistant(request):
    context={
    "previos_chatings1":"this is your previous chattings"
    }
    return render(request,'assistant.html', context)

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

def project_content(request,pk):
    project = Project.objects.get(project_id = pk)
    return render(request,'project.html', context={'project':project })

def show_roadmap(request):
    roadmap_url = f'/roadmap/{pk}'
    return redirect('roadmap_url')

roadmap_status = {}

def generate_roadmap(request,pk):
    global roadmap_status
    
    if pk in roadmap_status and roadmap_status[pk]:
        roadmap_content = Roadmap.objects.get(project_id = pk)
        lines = roadmap_content.generate_roadmap.split('\n')
        return render(request, 'roadmap.html', {'roadmap':roadmap_content, 'lines': lines})

    else:

        api_key = settings.OPENAI_SETTINGS['api_key']

    openai.api_key = api_key
    # Retrieve projects from the database
    project = Project.objects.get(project_id = pk)

    # Make request to OpenAI API
    response = openai.Completion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #             {"role": "system", "content": "You are a helpful assistant."},
    #             {"role": "user", "content": "Who won the world series in 2020?"},
    #             {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    #             {"role": "user", "content": "Where was it played?"}
    # ]

         engine="text-davinci-003",
         prompt=f"I want to make a project in {project.genre} which is I want to {project.title}.{project.description}. You have to make a roadmap for the project such a way that I can learn the required skills and then implement them. Keep the work as minimised as possible and be objective orientated. Properly define each step and tasks to be done in each step. Make sure your output has each step separated by /n and in each step, tasks should be separated useing ','. ",
         max_tokens=500,
         temperature=1,  
         n=1,  
         stop=None,
    )
    
    # Process the API response
    generated_roadmap = response.choices[0].text.strip()
    # Save the roadmap in the 'roadmap' database
    roadmap = Roadmap(
        generate_roadmap=generated_roadmap,
        title = project.title,
        description = project.description,
        skills = project.skills,
        genre = project.genre,
        project_id = project.project_id,
    )
    roadmap.save()

    roadmap_status[pk] = True
    lines = roadmap.generate_roadmap.split('\n')

    return render(request, 'roadmap.html', {'roadmap': roadmap, 'lines': lines})

# def show_roadmap(request, pk):
#     global roadmap_status

#     if pk in roadmap_status and roadmap_status[pk]:

#         roadmap_content = Roadmap.objects.get(project_id = pk)

#     return render(request, 'roadmap.html', {'roadmap':roadmap_content})